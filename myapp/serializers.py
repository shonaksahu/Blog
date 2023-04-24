from rest_framework import serializers
from myapp.models import Blog, Comment, User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'dob', 'email', 'joining_date', 'address', 'mobile_number', 'is_active', 'is_staff', 'is_superuser', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:  
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return {
                    'user_id': user.id,
                    'email': user.email,
                    'access_token': access_token,
                    'refresh_token': str(refresh)
                }
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
        
class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    comment = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'blog', 'parent_comment', 'created_at', 'replies', 'comment']
        read_only_fields = ['id', 'created_at', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

    def create(self, validated_data):
        comment = validated_data.pop('comment')
        user = self.context['request'].user
        blog = validated_data['blog']

        comment_obj = Comment.objects.create(
            content=comment,
            author=user,
            blog=blog,
            **validated_data
        )

        return comment_obj
    
    def validate(self, attrs):
        parent_comment = attrs.get('parent_comment', None) 

        if parent_comment and parent_comment.blog != attrs['blog']:
            raise serializers.ValidationError('The parent comment is not associated with the same blog.')
        return attrs