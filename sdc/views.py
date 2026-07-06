from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages


def addproject(request):
    if request.method == 'GET':
        return render(request,'sdc/addproject.html',{})
    if request.method == 'POST':
      pass
    
def projectallocation(request):
    if request.method == 'GET':
        return render(request,'sdc/projectallocation.html',{})
    if request.method == 'POST':
       pass

def documentupload(request):
    if request.method == 'GET':
        return render(request,'sdc/documentupload.html',{})
    if request.method == 'POST':
       pass

def projectdetails(request):
    if request.method == 'GET':
        return render(request,'sdc/projectdetails.html',{})
    if request.method == 'POST':
       pass

