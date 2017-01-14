from django.contrib import admin
from  cabs.models import CabDetails, UserProfile, TripTransactions

admin.site.register(CabDetails)
admin.site.register(TripTransactions)
admin.site.register(UserProfile)
