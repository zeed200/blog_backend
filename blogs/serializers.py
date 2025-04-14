from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class PostSerializar(serializers.ModelSerializer):
    author =  serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author1 = serializers.CharField(source='author.username')
    profile = serializers.ImageField(source='author.profile.image')
    count = serializers.IntegerField(source='comment.count', read_only=True)
   
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'post_date', 'author', 'profile', 'count', 'author1')




class CommentSerializar(serializers.ModelSerializer):

    
    class Meta:
        model = Comment
        fields = ('id', 'name', 'email', 'body', 'comment_date', 'active', 'post')        

        