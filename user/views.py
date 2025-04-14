from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from .models import Profile as ProfileModel
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from blogs.models import Post
import base64
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
from blogs.serializers import PostSerializar
# Create your views here.

class CreateUser(APIView): 
    def post(self, request):
        
        user = request.data
        serializer = UserSerializar(data={"username":user['username'],"email":user['email'],"first_name":user['first_name'],"last_name":user['last_name'],"password":user['password1']})
        if serializer.is_valid():
            serializer.save()   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginUser(APIView):
    def post(self, request):
        username = request.data.get("username") 
        password = request.data.get("password")  
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key})
        return Response({'error':'هناك خطأ في أسم المستخدم أو كلمة المرور'}, status=400)

class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
        
    def post(self, request):
        try:
            request.user.auth_token.delete()
            response = Response({"message":"تم تسجيل الخروج بنجاح"}, status=200)
            
            return response
        except Exception as e:
            return Response({"error":"حدث خطأ"}, status=500)

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        profile = ProfileModel.objects.get(user=request.user) 
        posts = Post.objects.filter(author=request.user)
        profile_data = ProfileSerializar(profile, context = {"request":request}, many=False).data
        posts_data = PostSerializar(posts, many=True).data
        count = Post.objects.filter(author=request.user).count()
        return Response({
            'profile':profile_data,
            'posts':posts_data,
            'count':count
        })
    
class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        profile = User.objects.get(id=request.user.id) 
        profile_data = UserSerializar(profile, context = {"request":request}, many=False).data
        return Response(profile_data)
    def put(self, request):
        profile = request.data
        image_data = profile['base64']
        # format, imgstr = image_data.split(';base64,')
        imgdata = base64.b64decode(image_data)
            
            # تحويل البيانات إلى محتوى ملف يمكن حفظه
        image_file = ContentFile(imgdata, name=f'{request.user.id}.png')
        # print(image_file)
        # # profile_image = request.files
        profile_user = User.objects.get(id=request.user)
        serializer = UserSerializar(profile_user, data={"email":profile['email'], "first_name":profile['first_name'], "last_name":profile['last_name']}, partial=True)
        pro_user = ProfileModel.objects.get(user=request.user)
        serializer_pro = ProfileSerializar(pro_user, data={"image":image_file}, partial=True)
        if serializer.is_valid() and serializer_pro.is_valid():
            serializer.save()
            serializer_pro.save()
 
            return Response(serializer.data, status=200)
        return Response(serializer.data, status=400)

    
    

