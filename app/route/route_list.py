from route.Index import Index
from route.Authentication import Authentication
from route.Logout import Logout
from route.Registration import Registration
from route.Routes import Route
from route.get_list import Test_route
from route.route_debug import Debug
from route.route_filter import RouteFilter
from route.route_geo import RouteGeo
from route.route_debug import Debug

__author__ = 'ar.chusovitin'

ROUTES = {
    Index: '/',
    RouteGeo: '/geo',
    Test_route: '/list',
    RouteFilter: '/filter',
    Authentication: '/auth',
    Registration: '/registration',
    Debug: '/debug',
    Logout: '/logout',
    Route: '/route'
}
