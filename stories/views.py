import io 
import os 
import json
import requests 
import firebase_admin
import google.generativeai as genai

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer 
from rest_framework.parsers import MultiPartParser
from django.http import HttpResponse, JsonResponse

from PIL import Image
from decouple import config
from uuid import uuid4
from firebase_admin import credentials, storage
from decouple import config


cred = credentials.Certificate('./taka.json')
firebase = firebase_admin.initialize_app(cred, {
    'storageBucket' : config('storageBucket')
})


def upload_audio_to_firebase(file_path, destination_path):    
    try:
        bucket = storage.bucket()
        blob   = bucket.blob(destination_path)
        blob.upload_from_filename(file_path)
        blob.make_public()

        return blob.public_url
    
    except Exception as e:
        print(f"Error uploading file: {e}")


# delete a file in a folder 
def delete_file_in_folder(folder_path, filename):
    try:
        file_path = os.path.join(folder_path, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")


class ExposeHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Expose-Headers'] = 'story'
        return response



def expose_headers(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            response['Access-Control-Expose-Headers'] = 'story'
        return response
    return wrapper


# configurations
genai.configure(api_key=config('GEMINI_KEY'))
model          = genai.GenerativeModel('gemini-1.0-pro-latest')
vision         = genai.GenerativeModel('gemini-pro-vision')
openai_api_key = config('OPENAI_KEY')


"""
1. endpoint generate story 
image or url required  
tone required 
prompt optional 

{
    title: str
    story: list of str
    audio: url 

}
"""

# functions 

def text_to_speech(message):
    filename = str(uuid4()) + '.mp3'

    url = "https://api.openai.com/v1/audio/speech"

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "tts-1",
        "input": message,
        "voice": "fable"
    }

    response = requests.post(url, headers=headers, json=data)
    filepath = f"voice_notes/{filename}"

    with open(filepath, "wb") as f:
        f.write(response.content)

    # save to firebase 
    url = upload_audio_to_firebase(filepath, filepath)
    delete_file_in_folder('.', filepath)
    
    return url 



def pollish_story(story, tone, uprompt=''):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages" : [
            {
                "role"    : "assistant",
                "content" : f"""You a big storyteller, you can take a text and pollish it 
                                to make a compelling story with a lot of emotions. You use
                                emojies in the story. You adapt the story with a {tone} tone.
                                Take into account this the comment = '{uprompt}'. If comment is not empty.
                                your response should always be in the following json format:
                                {{
                                    "title" : "title of the story",
                                    "story" : "list of paragraphs"

                                }}
                            """
            },
            {
                "role"    : "user",
                "content" : story
            },

        ],
        # "max_tokens": 100
    }

    response        = requests.post(url, headers=headers, json=data)
    response        = response.json()
    message_content = response['choices'][0]['message']['content']


    return message_content


def gemini_image_story(image):
    vision_response = vision.generate_content([f"Write a short story about this picture.", image],stream=True)
    vision_response.resolve()

    return vision_response.text


def gemini_url_story(url):
    image = Image.open(requests.get(url, stream=True).raw)
    vision_response = vision.generate_content(
        ["You a big storyteller, you can take a text and pollish it to make a compelling story with a lot of emotions. You use emojies in the story.", image],
        stream=True
    )
    vision_response.resolve()

    return vision_response.text


def gemini_image_or_url_story(type, content):
    if type == 'image':
        return gemini_image_story(image=content)
    elif type == 'url':
        return gemini_url_story(url=content)




@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer])
@parser_classes([MultiPartParser,])
@expose_headers
def story_from_image(request, type:str):
    if request.method == 'POST':
        if type == 'image':
            content       = request.FILES.get('image')
            image_content = Image.open(io.BytesIO(content.read()))
            image_info    = gemini_image_or_url_story(type='image', content=image_content)

        elif type =='url':
            content    = request.data.get('url')
            image_info = gemini_image_or_url_story(type='url', content=content)

        elif type is None:
            return Response({
                'message' : 'make sur you choose url or image'
            })
            
        tone    = request.data.get('tone', None)
        uprompt = request.data.get('prompt', None)
        try:
            story = pollish_story(image_info, tone=tone, uprompt=uprompt)
            
            story = json.loads(story)
            nuggets = "".join(story.get('story'))
            url = text_to_speech(nuggets)
            
            return Response({
                'story' : story,
                'url' : url 
            }, status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message' : 'Yes you can generate your stories here..'})
    


"""
dont say time never take 
ask for a speaker 
dont talk while the avatar is talking 

he is lives in cote d'ivoire or in cameroon 
we can improve more on the demo 

we add the avatar 
we show the roadmap 



"""