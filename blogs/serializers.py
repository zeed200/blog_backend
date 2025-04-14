from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


# class UserSerializar(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

class PostSerializar(serializers.ModelSerializer):
    author =  serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author1 = serializers.CharField(source='author.username')
    profile = serializers.ImageField(source='author.profile.image')
    count = serializers.IntegerField(source='comment.count', read_only=True)
    # author = UserSerializar(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'post_date', 'author', 'profile', 'count', 'author1')

    # def create(self, validated_data):
    #     # الحصول على اسم المؤلف من البيانات
    #     author_name = validated_data.pop('author')
        
    #     # إذا كان المؤلف موجودًا بالفعل في قاعدة البيانات
    #     author = User.objects.get(id=author_name)
        
    #     # إنشاء المنشور مع المؤلف
    #     post = Post.objects.create(author=author, **validated_data)
    #     return post    


class CommentSerializar(serializers.ModelSerializer):
    # post = PostSerializar(many=False,read_only=False)
    
    class Meta:
        model = Comment
        fields = ('id', 'name', 'email', 'body', 'comment_date', 'active', 'post')        

        