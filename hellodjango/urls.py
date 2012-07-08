from django.conf.urls import patterns, include, url
import hellodjango
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hellodjango.views.home', name='home'),
    # url(r'^hellodjango/', include('hellodjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'app.views.search', name='search'),
    url(r'^calpoly$', 'app.views.search', name='search'),
    url(r'^calpoly/sell$', 'app.views.sell', name='sell'),
    url(r'^calpoly/search$', 'app.views.search', name='search'),
    url(r'^calpoly/thanks$', 'app.views.thanks', name='thanks'), 
    url(r'^calpoly/contactseller$', 'app.views.contactseller', name='contactseller'),
    url(r'^calpoly/delete$', 'app.views.delete', name='delete'), 
    url(r'^calpoly/message$', 'app.views.messageSent', name='messageSent')
)
urlpatterns += patterns('',  
(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': hellodjango.settings.STATIC_ROOT}),  
)  
