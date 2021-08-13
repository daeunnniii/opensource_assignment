from django.shortcuts import render

def index(request):
    return render(request, 'mynote/fullnote.html')
