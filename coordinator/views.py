from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from helpermodule import studenthelper
from django.http import JsonResponse
import time
from urllib.parse import urlparse, parse_qs

def sdcdashboard(request):
    if request.method == 'GET':
        return render(request,'coordinator/sdcdashboard.html',{})
    if request.method == 'POST':
       pass

def registration(request):
    if request.method == 'GET':
        return render(request,'coordinator/registration1.html',{})
    if request.method == 'POST':
       pass

def temp(request):
    if request.method == 'GET':
        return render(request,'coordinator/typography-elements.html',{})
    if request.method == 'POST':
       pass

