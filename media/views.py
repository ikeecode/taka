from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework import status

from django.shortcuts import redirect

from pexels_api import API
from decouple import config 

# Create your views here.


# pexels configurations 

pexels = API(config('PEXELS_API_KEY'))
renderer_classes_var = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]

@api_view(['GET'])
@renderer_classes(renderer_classes_var)
def home(request):
    return Response({
        'message' : "Welcome to Taka API"
    })

@api_view(['GET'])
@renderer_classes(renderer_classes_var)
def photos(request, topic: str):
    photos = pexels.search(topic, page=1, results_per_page=5)
    print(photos)
    return Response(photos, status.HTTP_200_OK)


from pprint import pprint 
import requests 

from urllib.parse import urlparse, parse_qs

def get_next_page_number(url):
    page_number = parse_qs(urlparse(url=url).query).get('page')[0]
    return page_number



@api_view(['GET'])
@renderer_classes(renderer_classes_var)
def populars(request):
    photos = pexels.popular()
    url = photos.get('next_page')
    number = get_next_page_number(url=url)

    photos['next_page'] = f'https://taka-1.onrender.com/media/populars/{number}'


    return Response(photos, status.HTTP_200_OK)



@api_view(['GET'])
@renderer_classes(renderer_classes_var)
def next_page(request, page_number):
    if page_number > 1:
        photos = pexels.popular(page=page_number)

        url = photos.get('next_page')
        url2 = photos.get('prev_page')
        number = get_next_page_number(url=url)
        number2 = get_next_page_number(url=url2)

        photos['next_page'] = f'https://taka-1.onrender.com/media/populars/{number}'
        photos['prev_page'] = f'https://taka-1.onrender.com/media/populars/{number2}'


        return Response(photos, status.HTTP_200_OK)
    else:
        return redirect('populars')
    
