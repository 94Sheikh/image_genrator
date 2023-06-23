from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import os
import openai
import io
import requests
import PIL
from PIL import Image



# load apikey from the key.env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# set the openai key
openai.api_key = api_key

# Create your views here.
def image_genrator(request):
    if request.method == 'POST':
        text = request.POST['text']

        response = openai.Image.create(
            prompt = text,
            n = 1,
            size = '512x512'
        )
    # get the img url from the response
        img_url = response.data[0]['url']


    # pass the img url to the template

        context = {
            'title': 'image-genrator',
            'img_url': img_url,
            'text': text
        }

        return render(request, 'index.html', context)
    
    elif request.method == 'GET' and 'download' in request.GET:
        img_url = request.GET['download']
        
        # Download the image
        image_response = requests.get(img_url)
        image_content = image_response.content

        # Create a response with the image data and appropriate headers for download
        response = HttpResponse(image_content, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="generated_image.png"'

        return response
    return render(request, 'index.html')

