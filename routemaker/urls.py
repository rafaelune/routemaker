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

    # Pagina de retorno callback oauth
    url(r'^callback/$', 'routemaker.views.oauth_callback', name='callback'),

    # Ajax filtro de pedidos
    (r'^filtro/$', 'routemaker.views.pedidos_search'),

    # Ajax retorno de pedidos em json
    (r'^pedidos/$', 'routemaker.views.pedidos_json'),

    # Ajax atribui e retorna os terceiros dos pedidos em json
    (r'^cliente-pedido/$', 'routemaker.views.cliente_endereco_json'),

    # Pagina principal
    (r'^home/$', 'routemaker.views.home'),

    # Form de login
    (r'^login/$', 'routemaker.views.log_in'),

    # Logout url
    (r'^logout/$', 'routemaker.views.log_out'),

    # Homepage
    (r'^$', 'routemaker.views.index'),
)
