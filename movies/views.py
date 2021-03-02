from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

# Create your views here.

AT = Airtable('AIRTABLE_API_KEY',
              'Movies',
              api_key='AIRTABLE_MOVIESTABLE_BASE_ID')



def home_page(request):

    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    context = {
        'search_result': search_result,
    }
    return render(request, 'movies/movies_base.html', context)


def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://www.escapeauthority.com/wp-content/uploads/2116/11/No-image-found.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
            messages.success(request, 'New Movie Added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when trying to create a new movie: {}'.format(e))
    return redirect('/')

def update(request, movie_id):
    if request.method == 'POST':
        data={
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://www.escapeauthority.com/wp-content/uploads/2116/11/No-image-found.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.update(movie_id, data)
            messages.success(request, 'Movie updated: {}'.format(response['fields'].get('Name')) )
        except Exception as e:
            messages.warning(request, "Got a error when trying to update a movie: {}".format(e))
    return redirect('/')


def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        response = AT.delete(movie_id)
        messages.warning(request, 'Movie {} successfully deleted'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'Got an error when trying to delete a movie {}'.format(e))
    return redirect('/')
