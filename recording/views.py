import os
from django.http import JsonResponse as response
from django.shortcuts import render,redirect
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import PostAudio
from .postAudioSerializer import postAudioSerializer
import ast
import random

def index(request):
    file = open("recording/input.txt" ,encoding = "utf8").readlines()
    print(file)
    print(random.choice(file))
    return render(request,'index.html',{"sentence":random.choice(file)})


def deleteFiles(request,file_id):
    print("i hit !")
    file = PostAudio.objects.get(pk=file_id)
    os.remove(os.path.join("files",str(file.hotel_Main_Img)) )
    file.delete()
    return redirect('result')


def result(request):
    files=getFiles()
    files = ast.literal_eval(files.content.decode('utf-8'))
    dict = {"product": files}
    print(dict)
    return render(request,'result.html',dict)

def getFiles(request=None):
    results = PostAudio.objects.all()
    print(results.values())
    serializer = postAudioSerializer(results,many=True).data
    return response(serializer,safe=False)
    # return results


@csrf_exempt
def upload(request):
    print(upload)
    if request.method == 'POST':
        audio_Orm = PostAudio()
        # form = PostAudio(request.POST, request.FILES)
        name=request.FILES['ourfile'].name.split(".")[0].strip()
        name = name.replace("%0A","")
        audio_Orm.description =name
        request.FILES['ourfile'].name = str(datetime.now()) + request.FILES['ourfile'].name
        form = request.FILES['ourfile']
        audio_Orm.hotel_Main_Img = form

        audio_Orm.save()
        serializer = postAudioSerializer(audio_Orm, many=False).data
        return response(serializer,safe=False)