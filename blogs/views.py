from django.shortcuts import render, get_object_or_404
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class PostList(APIView):
 
    def get(self, request):
        posts = Post.objects.all()
        data = PostSerializar(posts, context = {"request":request}, many=True).data  
        return Response(data)





class PostDetail(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        auth = post.author == request.user
        data = PostSerializar(post,context = {"request":request}, many=False).data
        return Response({'data':data,'auth':auth})
    

class CommentPost(APIView):
    def get(self, request, post_id):
        Comments = Comment.objects.filter(post=post_id, active=True)
        data = CommentSerializar(Comments, many=True).data
        return Response(data)
    
    def post(self, request, post_id):
        comment = request.data
        serializer = CommentSerializar(data={"name":comment['name'],"email":comment['email'],"body":comment['body'],"post":comment['post']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePost(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        post = request.data
        author = request.user.id
        print(author)
        print(post)
        serializer = PostSerializar(data={"title":post['title'], "content":post['content'], "author":author}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePost(APIView):
     permission_classes = [IsAuthenticated]
     authentication_classes = [TokenAuthentication]
     def get(self, request, post_id):
        Posts = Post.objects.get(id=post_id)
        data = PostSerializar(Posts, many=False).data
        return Response(data)

     def put(self, request, post_id):
        post = request.data
        post_up = Post.objects.get(id=post_id)
        serializer = PostSerializar(post_up, data={"title":post['title'], "content":post['content']}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.error, status=400)
    

class PostDelete(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, post_id):
        Posts = Post.objects.get(id=post_id)
        data = PostSerializar(Posts, many=False).data
        return Response(data)

    def delete(self, request, post_id, format=None):
        try:
            post = Post.objects.get(id=post_id, author=request.user)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)