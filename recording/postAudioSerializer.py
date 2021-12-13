from rest_framework import serializers
from .models import PostAudio


class postAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAudio
        fields = '__all__'
