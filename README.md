# fuber_app
proprietor of fuber, an on call taxi service. API app to get info about nearby cabs and book one cab.


#APIS Available, 


1.  {{url}}/available-cars/  Request Method: POST Description: Get All Available cars nearby

Parameters:

latitude:
longitude:


Response :

{
  "nearest_cars": [
    {
      "cab_name": "Kaloor Taxi",
      "distance_para": 0.0433290796694301,
      "longitude": 76.302815,
      "cab_color": "",
      "latitude": 9.99709,
      "cab_no": "ABS12"
    },
    {
      "cab_name": "Kalloor Taxi",
      "distance_para": 0.0433290796694301,
      "longitude": 76.302815,
      "cab_color": "Pink",
      "latitude": 9.99709,
      "cab_no": "AZQ11"
    }
  ]
}

2.{{url}}/create-booking/ Request Method:POST Description: Assigns Nearsest car to requested user

Response:
If cabs available : {"status":"Trip Confirrmed","cab_no":"ABS12","transaction_id":13}

If cabs Unavailable :  {"status":"No cabs is available"}




Post parameters:

latitude:9.99709
longitude:76.302815
user_id:1
cab_color:False // if it is true ,customers are particular that they only ride around in pink cars, 
for hipster reasons will get pink cars.//


3.{{url}}/end-trip/ Request Method:POST Description: This ends trips under transactions

Post parameters:

end_latitude:10.015861
end_longitude:76.341867
transaction_id:10 // this mandatory, each trip have a transaction id. currently it PK.

Response:

{"status":"Trip Finished","cab_fee":13.552903985483155,"kms":4.276451992741578}

