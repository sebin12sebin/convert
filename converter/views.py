# converter/views.py

import os
import pygame
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import VideoToAudioForm
from moviepy.editor import *

pygame.mixer.init()

def handle_uploaded_file(f):
    with open('temp_video.mp4', 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def video_to_audio(input_file, output_file):
    try:
        video = VideoFileClip(input_file)
        audio = video.audio

        audio.write_audiofile(output_file, codec='mp3')

        audio.close()
        video.close()
        print(f"Audio extracted and saved as '{output_file}' successfully!")
        return f"Audio extracted and saved as '{output_file}' successfully!"
    except Exception as e:
        print("Error:", e)
        return f"Error: {e}"

def select_conversion_type(request):
    conversion_options = ['video_to_audio']  # Add more conversion options here if needed

    if request.method == 'POST':
        conversion_type = request.POST.get('conversion_type')
        return redirect('converter', conversion_type=conversion_type)
    
    return render(request, 'select_conversion.html', {'conversion_options': conversion_options})

def converter(request, conversion_type):
    supported_conversion_types = ['video_to_audio']  # Add more supported conversion types here if needed

    if conversion_type in supported_conversion_types:
        if request.method == 'POST':
            form = VideoToAudioForm(request.POST, request.FILES)
            if form.is_valid():
                input_file = request.FILES['video_file']
                output_file = form.cleaned_data['output_file'] + ".mp3"

                handle_uploaded_file(input_file)  # Save the uploaded file
                video_to_audio('temp_video.mp4', os.path.join(settings.MEDIA_ROOT, output_file))
                os.remove('temp_video.mp4')  # Delete the temporary video file after conversion

                audio_file_path = os.path.join(settings.MEDIA_URL, output_file)
                result_text = f"Audio extracted and saved as '{output_file}' successfully!"
                return render(request, 'converter.html', {'form': form, 'audio_file_path': audio_file_path, 'result_text': result_text})
        else:
            form = VideoToAudioForm()
    
        return render(request, 'converter.html', {'form': form})
    else:
        return HttpResponse("Unsupported conversion type.")
