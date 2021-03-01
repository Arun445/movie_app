from django.shortcuts import render
from django.contrib import messages
from airtable import Airtable
import os

# Create your views here.

AT = Airtable('appV8CGIdM2BlnEIK',
             'Movies',
             'keyoTyvNL7Iar7uFD')



def home_page(request):

    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    context = {
        'search_result': search_result,
    }
    return render(request, 'movies/movies_base.html', context)