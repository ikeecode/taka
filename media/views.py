from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework import status

from pexels_api import API
from decouple import config 

# Create your views here.


# pexels configurations 

pexels = API(config('PEXELS_API_KEY'))


@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer])
def photos(request, topic: str):
    photos = pexels.search(topic, page=1, results_per_page=5)
    print(photos)
    return Response(photos, status.HTTP_200_OK)



@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer])
def populars(request):
    photos = pexels.popular()
    return Response(photos, status.HTTP_200_OK)



