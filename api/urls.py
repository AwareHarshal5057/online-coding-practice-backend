
from django.urls import path
from . import views


urlpatterns = [

    # Home API
    path('', views.home_api, name='home_api'),

    # Authentication APIs
    path('register/', views.register_api, name='register_api'),
    path('login/', views.login_api, name='login_api'),
    path('logout/', views.logout_api, name='logout_api'),

    # Questions APIs
    path('questions/', views.questions_api, name='questions_api'),

    path(
        'questions/<int:pk>/',
        views.question_detail_api,
        name='question_detail_api'
    ),

    # Code Submission API
    path('submissions/', views.submissions_api, name='submissions_api'),

    path('mcq-questions/', views.mcq_questions_api, name='mcq_questions_api'),

    path('mcq-submit/',views.mcq_submit_api,name='mcq_submit_api'),
    path('mcq-results/',views.mcq_results_api,name='mcq_results_api'),

    # Python Lessons API
    path('lessons/', views.lessons_api, name='lessons_api'),
]
