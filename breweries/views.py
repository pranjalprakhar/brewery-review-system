from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse , Http404
import datetime
from .models import Review
from .forms import ReviewForm

import requests

def getstarted(request):
    return render(request, 'getstarted.html')


def product_page(request):
    return render(request, 'product.html')


def about_us(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def home_view(request):
    return render(request, 'base.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            return redirect('signup')
    context = {}
    return render(request, 'login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('login')
    
      
def search_view(request):
    return render(request, 'search.html')


def list_brewery(request):
    query = request.GET.get('query')
    breweries = []
    if query:
        response = requests.get(f'https://api.openbrewerydb.org/breweries/search?query={query}')
        breweries = response.json()

    for brewery in breweries:
        # Fetch reviews for the current brewery
        reviews = Review.objects.filter(brewery_id = brewery['id'])
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = int(total_rating / reviews.count())
        else:
            average_rating = 0
        brewery['average_rating'] = average_rating
    return render(request, 'list_brewery.html', {'breweries': breweries})

        
def brewery_detail_view(request, brewery_id):
    try:
        response = requests.get(f'https://api.openbrewerydb.org/breweries/{brewery_id}')
        response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
    except requests.exceptions.RequestException as e:
        raise Http404("Brewery not found") from e

    brewery = response.json()

    if not brewery:
        raise Http404("Brewery not found")
    reviews = Review.objects.filter(brewery_id=brewery_id)
    
    return render(request, 'brewery_detail.html', {'brewery': brewery})


def display_detail(request, brewery_id):
    try:
        response = requests.get(f'https://api.openbrewerydb.org/breweries/{brewery_id}')
        response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
    except requests.exceptions.RequestException as e:
        raise Http404("Brewery not found") from e

    brewery = response.json()
    reviews = Review.objects.filter(brewery_id = brewery_id)
    if reviews.exists():
        total_rating = sum(review.rating for review in reviews)
        print(f"Total rating: {total_rating}" )
        average_rating = int(total_rating / reviews.count())
    else:
        average_rating = 0
    brewery['average_rating'] = average_rating

    return render(request, 'display_detail.html', {'brewery': brewery, 'reviews': reviews})


def add_review(request, brewery_id):
    rating = request.POST.get('rating')
    description = request.POST.get('description')
    user = request.POST.get('user')

    review = Review.objects.create(
        brewery_id = brewery_id,
        rating=rating,
        description=description,
        user = user  # Assuming user is authenticated
    )

    return redirect('display_detail', brewery_id = brewery_id )
