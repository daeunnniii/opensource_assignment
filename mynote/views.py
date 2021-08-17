from django.shortcuts import render
from addnote.models import Note

def index(request):
    note_list = Note.objects.order_by('-reg_date')
    context = {'note_list':note_list}
    return render(request, 'mynote/fullnote.html', context)
