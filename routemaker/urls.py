from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'routemaker.views.home', name='home'),
    # url(r'^routemaker/', include('routemaker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Ajax filtro de pedidos
    (r'^filtro/$', 'routemaker.views.pedidos_search'),

    # Pagina principal
    (r'^home/$', 'routemaker.views.home'),

    # Form de cadastro
    (r'^cadastro/$', 'routemaker.views.signup'),

    # Form de login
    (r'^login/$', 'routemaker.views.log_in'),

    # Logout url
    (r'^logout/$', 'routemaker.views.log_out'),

    # Homepage
    (r'^$', 'routemaker.views.index'),
)
