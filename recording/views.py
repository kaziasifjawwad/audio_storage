import os
from django.http import JsonResponse as response, HttpResponse, Http404
from django.shortcuts import render,redirect
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import PostAudio
from .postAudioSerializer import postAudioSerializer
import ast
import random
import shutil
def index(request):
    file = open("recording/input.txt" ,encoding = "utf8").readlines()
    # print(file)
    # print(random.choice(file))
    return render(request,'index.html',{"sentence":random.choice(file)})


def deleteFiles(request,file_id):
    # print("i hit !")
    file = PostAudio.objects.get(pk=file_id)
    os.remove(os.path.join("files",str(file.hotel_Main_Img)) )
    file.delete()
    return redirect('result')


def result(request):
    files=getFiles()
    files = ast.literal_eval(files.content.decode('utf-8'))
    dict = {"product": files}
    # print(dict)
    return render(request,'result.html',dict)

def getFiles(request=None):
    results = PostAudio.objects.all()
    # print(results.values())
    serializer = postAudioSerializer(results,many=True).data
    return response(serializer,safe=False)
    # return results


@csrf_exempt
def upload(request):
    # print(upload)
    if request.method == 'POST':
        audio_Orm = PostAudio()
        # form = PostAudio(request.POST, request.FILES)
        name=request.FILES['ourfile'].name.split(".")[0].strip()
        name = name.replace("%0A","")
        audio_Orm.description =name
        request.FILES['ourfile'].name = str(datetime.now())+".wav"
        form = request.FILES['ourfile']
        audio_Orm.hotel_Main_Img = form

        audio_Orm.save()
        serializer = postAudioSerializer(audio_Orm, many=False).data
        return response(serializer,safe=False)

def dataset(request):
    # print(os.listdir("files\\static\\media"))
    # print("hello there !")
    result = open('files\\static\\result.txt', 'w' , encoding="utf-8")
    string=""
    results = PostAudio.objects.all()
    for item in results:
        description = item.description
        file_name = str(item.hotel_Main_Img).split("/")[-1]
        string=string+"{}    {}\n".format(file_name,description)
    result.write(string)
    print(result)
    result.close()
    shutil.make_archive("dataset", 'zip', 'files\\static')
    file_path ='dataset.zip'
    open(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    return HttpResponse({"a":1})