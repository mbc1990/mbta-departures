from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # TODO: How long to keep "departed" trains around for? 
    return HttpResponse("Hello, world. You're at the departures index.")
