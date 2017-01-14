from django.conf.urls import patterns, include, url
from django.contrib import admin
from cabs.views import AvailableCars,CreateABookingRequest, EndTrip

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fuber_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^available-cars/$',AvailableCars.as_view()),
    url(r'^create-booking/$',CreateABookingRequest.as_view()),
    url(r'^end-trip/$',EndTrip.as_view()),
)
