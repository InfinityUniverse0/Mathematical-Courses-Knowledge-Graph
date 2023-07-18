from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from py2neo import Graph, Node, Relationship
import openai
import json
openai.api_key = settings.OPENAI_API_KEY

# Create your views here.
def page_not_found(request, exception):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')


def index_page(request):
    return render(request, 'index.html')


def chat(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')

        try:
            data = json.loads(body)
            message = data.get('message')
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)

        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {'role': 'user', 'content': message}
                ]
            )
            completion = response['choices'][0]['message']['content']
        except Exception as e:
            completion = 'ERROR: ' + str(e)

        return JsonResponse({'completion': completion})

    return render(request, 'chat.html')

