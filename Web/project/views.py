from django.shortcuts import render
from django.conf import settings
from py2neo import Graph, Node, Relationship
import openai
openai.api_key = settings.OPENAI_API_KEY

# Create your views here.
def page_not_found(request, exception):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')


def index_page(request):
    return render(request, 'index.html')
