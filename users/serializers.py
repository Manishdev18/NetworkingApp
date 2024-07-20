from rest_framework import serializers
from .models import CustomUser, Friend, FriendRequest



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["password",  "first_name", "email" , "last_name"]
        extra_kwargs = {'password': {'write_only': True}}
    def validate_email(self, value):
        return value.lower()

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user



class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number']



class FriendRequestSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at', 'sender_name', 'receiver_name']
        read_only_fields = ['created_at', 'updated_at', 'sender_name', 'receiver_name']
    
    def get_sender_name(self, obj):
        return f'{obj.sender.first_name} {obj.sender.last_name}'

    def get_receiver_name(self, obj):
        return f'{obj.receiver.first_name} {obj.receiver.last_name}'



class FriendSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    friend_name = serializers.SerializerMethodField()
    class Meta:
        model = Friend
        fields = ['id', 'user', 'friend', 'created_at', 'user_name', 'friend_name']
        read_only_fields = ['user', 'created_at', 'user_name', 'friend_name']
    def get_user_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def get_friend_name(self, obj):
        return f'{obj.friend.first_name} {obj.friend.last_name}'
