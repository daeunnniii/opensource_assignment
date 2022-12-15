from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteEditForm
from addnote.models import Note
from addnote import textrank_word2vec
from django.http import JsonResponse
from django.urls import reverse
import librosa
import soundfile as sf

import urllib3
import json
import base64

from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='common:login')
def index(request):
    return render(request, 'addnote/making_note.html')

@login_required(login_url='common:login')
def saveNote(request):
    user_input_str = request.POST['file_route']
    note = Note()
    note.user = request.user
    note.subject = request.POST['subject']
    note.note_description = request.POST['note_description']
    note.reg_date=timezone.now()
    note.audio = request.FILES['audio']
    note.save()

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = "b1a210f3-f6fd-4fab-8819-0e47149b2a92"
    languageCode = "korean"
    
    sr = 16000
    sec = 30
    y, sr = librosa.load('./media/audio/'+user_input_str, sr=sr)
    test = round(len(y)/sr)
    strResult = ""
    
    for i in range(0, test, 10):
        file_name = str(datetime.now().microsecond)
        ny = y[sr*i:sr*(i+10)]
        sf.write('./media/result/'+file_name+'.wav', ny, sr, format='WAV', endian='LITTLE', subtype='PCM_16') # 깨지지 않음

        audioFilePath = './media/result/'+file_name+'.wav'
        file = open(audioFilePath, "rb")
        audioContents = base64.b64encode(file.read()).decode("utf8")
        file.close()

        requestJson = {
            "access_key": accessKey,
            "argument": {
                "language_code": languageCode,
                "audio": audioContents
            }
        }

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
        )
        try:
            jsonObject = json.loads(str(response.data,"utf-8"))
            strResult = strResult + str(jsonObject.get("return_object").get("recognized"))
        except:
            pass
    n = Note.objects.get(id=note.id)
    n.sttText = strResult
    n.save()
    
    return redirect(n.id)

@login_required(login_url='common:login')
def result(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    form = NoteEditForm(instance=note)
    context = {'note' : note, 'form' : form}
    return render(request, 'addnote/mynote_detail.html', context)

@login_required(login_url='common:login')
def view_network(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if (note.vis_js_nodes == '' or note.vis_js_nodes is None) and (note.vis_js_edges == '' or note.vis_js_edges is None):
        text = note.sttText
        nodes_request, edges_request = textrank_word2vec.textrank_w2v_to_vis(text)
        note.vis_js_nodes = nodes_request
        note.vis_js_edges = edges_request
        note.save()
    else:
        nodes_request, edges_request = note.vis_js_nodes, note.vis_js_edges
    context = {'result': 'success', 'nodes':nodes_request, 'edges':edges_request}
    return JsonResponse(context)

@login_required(login_url='common:login')
def addnote_save(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == "POST":
        form = NoteEditForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.vis_js_nodes, note.vis_js_edges = textrank_word2vec.textrank_w2v_to_vis(note.sttText)
            note.save()
            return redirect('mynote:index')
    else:
        form = NoteEditForm(instance=note)
        context = {'note' : note, 'form' : form}
    return HttpResponseRedirect(reverse('addnote:result'), args=note.id)