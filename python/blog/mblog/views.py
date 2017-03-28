from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import datetime

# Create your views here.
def home(request):
   context = {

   }
   return render(request, "mblog/home.html", context)

def demo(request):
   context = {

   }
   return render(request, "mblog/jevelin_demo.html", context)
