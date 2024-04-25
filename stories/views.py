from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer 
from rest_framework.parsers import MultiPartParser

from PIL import Image
from decouple import config

import io 
import requests 
import google.generativeai as genai



# configurations

genai.configure(api_key=config('GEMINI_KEY'))
model = genai.GenerativeModel('gemini-1.0-pro-latest')
vision = genai.GenerativeModel('gemini-pro-vision')





# functions 

def gemini_image_story(image):
    vision_response = vision.generate_content([f"Write a short story about this picture.", image],stream=True)
    vision_response.resolve()

    return vision_response.text


def write_something(libelle, url):
    image = Image.open(requests.get(url, stream=True).raw)
    vision_response = vision.generate_content(
        [f"Write a short {libelle} about this picture.", image],
        stream=True
    )
    vision_response.resolve()

    return vision_response.text


def generate_words(number_of_word, url):
    image = Image.open(requests.get(url, stream=True).raw)
    vision_response = vision.generate_content(
        [f"Give me {number_of_word} words about this picture.", image],
        stream=True
    )
    vision_response.resolve()

    return vision_response.text



@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer])
@parser_classes([MultiPartParser,])
def create_upload_file(request):
    if request.method == 'POST':
        content = request.FILES.get('image')

        try:
            image_content = Image.open(io.BytesIO(content.read()))
            image_info = gemini_image_story(image_content)

            return Response(image_info, status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message' : 'Yes you can generate your stories here..'})