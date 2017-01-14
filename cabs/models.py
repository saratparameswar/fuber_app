from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from django.template.defaultfilters import default

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='profile_user')
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    
    latitude = models.DecimalField(default=0.0,decimal_places=20,max_digits=30,blank=True,null=True)
    longitude = models.DecimalField(default=0.0,decimal_places=20,max_digits=30,blank=True,null=True)
    
    def __unicode__(self):
        return self.user.username



CAB_COLOR = (
        ('Pink', 'Pink'),
        ('White',  'White'),
    )


class CabDetails(models.Model):
    cab_name = models.CharField(max_length=128, blank=True)
    cab_no = models.CharField(max_length=128)
    latitude = models.DecimalField(default=0.0,decimal_places=20,max_digits=30,blank=True,null=True)
    cab_color = models.CharField(max_length=128, blank=True, choices = CAB_COLOR,)
    longitude = models.DecimalField(default=0.0,decimal_places=20,max_digits=30,blank=True,null=True)
    is_available = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.cab_name


"""All the state of trips"""

TRIP_STATUS = (
        ('Trip Confirmed', 'Trip Confirmed'),
        ('Cab Assigned', 'Cab Assigned'),
        ('Trip Cancelled',  'Trip Cancelled'),
        ('Trip Finished',  'Trip Finished'),
    )
    
class TripTransactions(models.Model):
    cab = models.ForeignKey(CabDetails)
    userProfile = models.ForeignKey(UserProfile)
    start_latitude = models.DecimalField(default=0.0,decimal_places=20,max_digits=30,blank=True,null=True)
    start_longitude = models.DecimalField(default=0.0,decimal_places=20,max_digits=30,blank=True,null=True)
    end_latitude = models.DecimalField(default=0.0,decimal_places=20,max_digits=30,blank=True,null=True)
    end_longitude = models.DecimalField(default=0.0,decimal_places=20,max_digits=30,blank=True,null=True)
    trip_status = models.CharField(max_length=128, null=True, blank=True, choices = TRIP_STATUS,)
    
    trip_start_time = models.DateTimeField(blank=True,null=True)
    trip_end_time = models.DateTimeField(blank=True,null=True)
    price = models.CharField(max_length=128,null=True, blank=True)