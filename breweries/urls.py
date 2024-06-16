from django.urls import path
from .views import home_view, signup_view, login_view, logout_view, search_view, brewery_detail_view, add_review, getstarted, list_brewery, display_detail, product_page, about_us
from .views import contact


urlpatterns = [
    path('', home_view, name='home'),
    path('getstarted/', getstarted, name='getstarted'),
    path('product/', product_page, name='product'),
    path('about/', about_us, name='about'),
    path('contact/', contact, name='contact'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search/', search_view, name='search'),
    path('list_brewery', list_brewery, name='list_brewery'),
    path('brewery/<uuid:brewery_id>/', brewery_detail_view, name='brewery_detail_view'),
    path('display_detail/<uuid:brewery_id>/', display_detail, name='display_detail'),
    path('brewery/<uuid:brewery_id>/review', add_review, name='add_review'),
]