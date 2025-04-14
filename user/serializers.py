from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializar(serializers.ModelSerializer):
    profile = serializers.ImageField(source='profile.image')
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'profile')
        
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
       
        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)
        email = validated_data.get('email', instance.last_name)
       

        
        instance.first_name = first_name
        instance.last_name = last_name
        instance.email = email
      
        instance.save()

        return instance    

class ProfileSerializar(serializers.ModelSerializer):
    user = UserSerializar(many=False)
   
    
    class Meta:
        model = Profile
        fields = ('user', 'image')  


    def update(self, instance, validated_data):
      
        user_data = validated_data.pop('user', None)
        if user_data:
            instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
            instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
            instance.user.email = validated_data.get('email', instance.user.email)
            instance.user.save()

        return super().update(instance, validated_data)    


           