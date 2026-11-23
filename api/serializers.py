from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Question
from .models import CodeSubmission
from .models import MCQQuestion,MCQOption,MCQSubmission

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        username = data.get('username')
        password = data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password"
            )

        data['user'] = user

        return data



class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question

        fields = [
            'id',
            'title',
            'description',
            'difficulty',
            'sample_input',
            'sample_output',
            'created_at'
        ]

class CodeSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodeSubmission

        fields = [
            'id',
            'student',
            'question',
            'submitted_code',
            'submitted_at'
        ]

        read_only_fields = [
            'id',
            'student',
            'submitted_at'
        ]  

class MCQOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQOption
        fields = ['id','option_text']

class MCQQuestionSerializer(serializers.ModelSerializer):
    options = MCQOptionSerializer(many=True, read_only=True)

    class Meta:
        model = MCQQuestion
        fields = [
            'id',
            'question',
            'difficulty',
            'options'
        ]   

class MCQSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQSubmission
        fields =[
            'id',
            'question',
            'selected_option',
            'is_correct',
            'submitted_at'
        ] 
        read_only_fields = [
            'id',
            'is_correct',
            'submitted_at'
        ]                

    def validate(self, data):
        question = data['question'] 
        selected_option = data['selected_option']

        if selected_option.question != question:
            raise serializers.ValidationError(
                "selected option does not belong to this question"
            )
        return data     

    def create(self, validated_data):

        selected_option = validated_data['selected_option']

        validated_data['is_correct'] = selected_option.is_correct

        return MCQSubmission.objects.create(**validated_data)     


# print("AUTH USER:", request.user)
# print("AUTHENTICATED:", request.user.is_authenticated)
# print("AUTH HEADER:", request.META.get("HTTP_AUTHORIZATION"))    