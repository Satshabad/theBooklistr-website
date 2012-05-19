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

    
    url(r'^$', 'app.views.index'),
    url(r'^sell$', 'app.views.sell', name='sell')
)
urlpatterns += patterns('',  
(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': hellodjango.settings.STATIC_ROOT}),  
)  
