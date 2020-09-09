from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id' , 'content']

    def validate_content(self, value):
        if len(value) > 240:
            raise serializers.ValidationError("Too big tweet")
        return value