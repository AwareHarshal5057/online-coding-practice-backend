
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)

from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authtoken.models import Token

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    QuestionSerializer,
    CodeSubmissionSerializer
)

from .models import Question, CodeSubmission


# Home API
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def home_api(request):

    data = {
        "message": "welcome to online coding practice api",
        "status": "success"
    }

    return Response(data, status=status.HTTP_200_OK)


# Register API
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register_api(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "message": "Registration successful!",
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# Login API
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_api(request):

    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "Login successful!",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            },
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# Questions API - GET and POST
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def questions_api(request):

    # GET: Anyone can view questions
    if request.method == 'GET':

        questions = Question.objects.all()

        serializer = QuestionSerializer(
            questions,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST: Login required to add questions
    elif request.method == 'POST':

        if not request.user.is_authenticated:

            return Response(
                {"detail": "Please login to add a question."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Single Question API - GET, PUT, PATCH and DELETE
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def question_detail_api(request, pk):

    try:

        question = Question.objects.get(pk=pk)

    except Question.DoesNotExist:

        return Response(
            {"error": "Question not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET: Anyone can view a question
    if request.method == 'GET':

        serializer = QuestionSerializer(question)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # Login required for PUT, PATCH and DELETE
    if not request.user.is_authenticated:

        return Response(
            {"detail": "Please login to modify a question."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    elif request.method in ['PUT', 'PATCH']:

        serializer = QuestionSerializer(
            question,
            data=request.data,
            partial=(request.method == 'PATCH')
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':

        question.delete()

        return Response(
            {"message": "Question deleted successfully"},
            status=status.HTTP_200_OK
        )


# Code Submission API
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def submissions_api(request):

    # GET: Student submissions
    if request.method == 'GET':

        submissions = CodeSubmission.objects.filter(
            student=request.user
        )

        serializer = CodeSubmissionSerializer(
            submissions,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST: Submit code
    elif request.method == 'POST':

        serializer = CodeSubmissionSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(student=request.user)

            return Response(
                {
                    "message": "Code submitted successfully!",
                    "submission": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Logout API
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_api(request):

    request.auth.delete()

    return Response(
        {"message": "Logout successful!"},
        status=status.HTTP_200_OK
    )
