import math
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from math import radians, cos, sin, asin, sqrt
import gpxpy.geo

from cabs.models import CabDetails,TripTransactions, UserProfile
from datetime import timedelta



"""This object which have help to use for calculating parameters"""
class  CalculateDistance(object):
    
    def __init__(self,*args,**kwargs):
        print kwargs
        self.latitude_x1 = float(kwargs['latitude_x1'])
        self.longitude_y1 = float(kwargs['latitude_y1'])

   
    def calculate_distance(self,latitude_x2,longitude_y2):
        dist = math.sqrt( (latitude_x2 - self.latitude_x1)**2 + (longitude_y2 - self.longitude_y1)**2 )
        return dist
    
    def available_cars(self):
        cabs_avail =  CabDetails.objects.filter(is_available=True)
        cabs_available = []
        for cabs in cabs_avail:
            cab_details  = {}
            cab_details['cab_name'] = cabs.cab_name
            cab_details['cab_no'] = cabs.cab_no
            cab_details['cab_color'] = cabs.cab_color
            cab_details['latitude'] = float(cabs.latitude)
            cab_details['longitude'] = float(cabs.longitude)
            distance_para = self.calculate_distance(latitude_x2= cab_details['latitude'], longitude_y2= cab_details['longitude'])
            cab_details['distance_para'] = distance_para
            cabs_available.append(cab_details)
        near_by_cars = sorted(cabs_available, key=lambda k: k['distance_para'])
        return  near_by_cars
    
    def available_pink_cars(self, pink=True):
        cabs_avail =  CabDetails.objects.filter(cab_color='Pink',is_available=True)
        cabs_available = []
        for cabs in cabs_avail:
            cab_details  = {}
            cab_details['cab_name'] = cabs.cab_name
            cab_details['cab_no'] = cabs.cab_no
            cab_details['latitude'] = float(cabs.latitude)
            cab_details['longitude'] = float(cabs.longitude)
            distance_para = self.calculate_distance(latitude_x2= cab_details['latitude'], longitude_y2= cab_details['longitude'])
            cab_details['distance_para'] = distance_para
            cabs_available.append(cab_details)
        near_by_cars = sorted(cabs_available, key=lambda k: k['distance_para'])
        return  near_by_cars
    
    @staticmethod 
    def _calculate_distance(lat1,lon1,lat2,lon2):
        """use the equirectangular distance approximation. This approximation is faster than using the Haversine formula."""
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        
        lat2 =radians(lat2)
        lon2 = radians(lon2)
        
        R = 6371  # approximate radius of earth in km
        
        x = (lon2 - lon1) * cos( 0.5*(lat2+lat1) )
        y = lat2 - lat1
        kms = R * sqrt( x*x + y*y )
        return kms
    
    @staticmethod
    def cab_fee(in_kms, total_mins, color):
        total_fare = in_kms*2
        if color == 'Pink':
            total_fare  +=5
        return total_fare


class AvailableCars(APIView):
    
    def post(self, request, format=None):
        context_dict =  {}        
        user_postion_latitude = request.data['latitude']
        user_postion_longitude = request.data['longitude']
        
        cal_obj = CalculateDistance(latitude_x1=user_postion_latitude,latitude_y1=user_postion_longitude)
        if 'cab_color' in request.data:
            
            context_dict['nearest_cars'] = cal_obj.available_pink_cars(pink=True)
        else:
            context_dict['nearest_cars'] = cal_obj.available_cars()
        return Response(context_dict, status=status.HTTP_200_OK)
    
    


class CreateABookingRequest(APIView):
    
    def post(self, request, format=None):
        context_dict = {}
        pinky = None
        latitude =  request.data['latitude']
        longitude = request.data['longitude']
        cab_color = request.data['cab_color']
        user_id = request.data['user_id']
        
        cal_obj = CalculateDistance(latitude_x1=latitude,latitude_y1=longitude)
        if cab_color  == 'True':
            near_by = cal_obj.available_pink_cars(pink=True)
            pinky = True
        else:
            near_by = cal_obj.available_cars()
            
        """Nearby cab  is assigned"""
        if len(near_by) > 0:
            assigned_cab =  CabDetails.objects.get(cab_no=near_by[0]['cab_no'])
            user_obj  = UserProfile.objects.get(id=user_id)
            
            """Creating Transaction object with assignment details"""
            transaction_obj = TripTransactions(cab=assigned_cab,userProfile=user_obj,
                                               start_latitude=latitude,start_longitude=longitude,
                                               trip_status='Trip Confirmed',trip_start_time=datetime.datetime.now()
                                               )
            transaction_obj.save()
            
            """Now  mark the cab as inactive, since it is assigned"""
            assigned_cab.is_available = False
            assigned_cab.save()
            context_dict['status']  = 'Trip Confirrmed'
            context_dict['transaction_id']  = transaction_obj.id
            context_dict['cab_no']  = assigned_cab.cab_no
        else:
            context_dict['status']  = 'No cabs is available'
            if pinky == True:
                context_dict['status']  = 'No pink cabs is available'
           

        return Response(context_dict, status=status.HTTP_200_OK)
    
    
class EndTrip(APIView):
    
    def post(self, request, format=None):
        context_dict = {}
        transaction_id =  request.data['transaction_id']
        end_latitude = request.data['end_latitude']
        end_longitude = request.data['end_longitude']
        
        
        try:
            transaction_obj = TripTransactions.objects.get(id=transaction_id)
        except:
            transaction_obj = None
            
        """After Ending Trip, Update Transaction object"""
        if transaction_obj:
            transaction_obj.trip_end_time = datetime.datetime.now()
            transaction_obj.trip_status = 'Trip Finished'
            transaction_obj.end_latitude = end_latitude
            transaction_obj.end_longitude = end_longitude
            transaction_obj.save()
            """Make cab Available for booking"""
            transaction_obj.cab.is_available = True
            transaction_obj.cab.save()
            
            in_kms = CalculateDistance._calculate_distance(transaction_obj.start_latitude, transaction_obj.start_longitude, 
                                                  float(end_latitude), float(end_longitude))

            fare =  CalculateDistance.cab_fee(in_kms, total_mins=3, color=transaction_obj.cab.cab_color)
            context_dict['status'] = 'Trip Finished'
            context_dict['kms'] = in_kms
            context_dict['cab_fee'] =  fare
            
        return Response(context_dict, status=status.HTTP_200_OK)
    
    
