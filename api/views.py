
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)

from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
)

from rest_framework.authtoken.models import Token

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    QuestionSerializer,
    CodeSubmissionSerializer,
    LessonSerializer,
)

from .models import Question, CodeSubmission
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import MCQQuestionSerializer
from .models import MCQQuestion,MCQSubmission
from .serializers import MCQSubmissionSerializer

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
        user = serializer.save()

        return Response(
            {
                "message": "Registration successful!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# Login API (JWT Authentication)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_api(request):

    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful!",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
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

# Questions API
# GET: Public
# POST: JWT required

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def questions_api(request):

    if request.method == 'GET':

        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
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


# Single Question API
# GET: Public
# PUT/PATCH/DELETE: JWT required

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def question_detail_api(request, pk):

    try:
        question = Question.objects.get(pk=pk)

    except Question.DoesNotExist:
        return Response(
            {"error": "Question not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = QuestionSerializer(question)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def submissions_api(request):

    print("AUTH USER:", request.user)
    print("AUTHENTICATED:", request.user.is_authenticated)
    print("AUTH HEADER:", request.META.get("HTTP_AUTHORIZATION"))


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

    serializer = CodeSubmissionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(student=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



# Logout API (Old DRF Token Authentication)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_api(request):

    request.auth.delete()

    return Response(
        {"message": "Logout successful!"},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def mcq_questions_api(request):

    questions = MCQQuestion.objects.all()

    serializer = MCQQuestionSerializer(
        questions,
        many=True
    )

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def mcq_submit_api(request):

    serializer = MCQSubmissionSerializer(
        data=request.data
    )

    if serializer.is_valid():

        submission = serializer.save(
            student=request.user
        )

        return Response({
            "message": "Answer submitted successfully!",
            "is_correct": submission.is_correct
        }, status=status.HTTP_201_CREATED)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def mcq_results_api(request):

    submissions = MCQSubmission.objects.filter(
        student=request.user
    )

    serializer = MCQSubmissionSerializer(
        submissions,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )

# Published Python Lessons API
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def lessons_api(request):
    lessons = Lesson.objects.filter(is_published=True)

    serializer = LessonSerializer(
        lessons,
        many=True,
        context={'request': request}
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
