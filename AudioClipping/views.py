from django.shortcuts import render
from django.http import HttpResponse
from AudioClipping.functions import handle_uploaded_file
from AudioClipping.forms import StudentForm
from AudioClipping.AudioClippingScript import *
import glob
from scipy.io import wavfile
import scipy.signal as sps
import numpy as np
from scipy.io.wavfile import write



def index2(request):
    if request.method == 'POST':
        student = StudentForm(request.POST, request.FILES)
        if student.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("File uploaded successfuly")
    else:
        student = StudentForm()
        return render(request,"AudioClipping.html",{'form':student})

def AudioClipping(request):
    non_clipped_folder = 'files/'
    file_path = ''
    for file in glob.glob(non_clipped_folder+'*.wav'):
        file_path = str(file)
        print(file_path)

    new_rate = 48000
    sampling_rate, data = wavfile.read(file_path)
    number_of_samples = round(len(data)*float(new_rate)/sampling_rate)
    data = sps.resample(data, number_of_samples)
    write(file_path, new_rate, data.astype(np.int16))
    print(sampling_rate)

    audio, sample_rate = read_wave(file_path)
    print(sample_rate)
    vad = webrtcvad.Vad(2)
    print('sd')
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)
    segments = vad_collector(sample_rate, 30, 300, vad, frames)
    for i, segment in enumerate(segments):
        path = 'VS_recording/static/media/chunk-%00d.wav'%(i,)
        print(' Writing %s'%(path,))
        write_wave(path, segment, sample_rate)
    path = path.replace('VS_recording', '')
    path = path.replace("\\", "/")
    context = {
        "ClippedAudio": path
    }
    return render(request, 'AudioClippingDone.html', context)


def AudioClippingAdminStart(request):
    non_clipped_folder = 'VS_recording/static/media/'
    for file in glob.glob(non_clipped_folder+'*.wav'):
        file_path = str(file)

    file_path = file_path.replace('VS_recording', '')
    file_path = file_path.replace("\\", "/")
    print(file_path)

    context = {
        "filePath": file_path
    }

    return render(request, "AudioClippingAdminStart.html", context)

