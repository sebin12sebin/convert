# converter/forms.py

from django import forms

class VideoToAudioForm(forms.Form):
    video_file = forms.FileField(label='Video File', required=True)
    output_file = forms.CharField(label='Output File', max_length=100, required=True)
