
from django.conf import settings
from django.db import models


class Question(models.Model):

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField()

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='Easy'
    )

    sample_input = models.TextField()

    sample_output = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CodeSubmission(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='code_submissions'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    submitted_code = models.TextField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.question.title}"


class MCQQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy','Easy'),
        ('Medium','Medium'),
        ('Hard','Hard'),
    ]

    question = models.TextField()
    difficulty = models.CharField(max_length=10,choices=DIFFICULTY_CHOICES,default='Easy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class MCQOption(models.Model):
    question = models.ForeignKey(MCQQuestion,on_delete=models.CASCADE,related_name='options')  

    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text  


class MCQSubmission(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        MCQQuestion,
        on_delete=models.CASCADE
    )

    selected_option = models.ForeignKey(
        MCQOption,
        on_delete=models.CASCADE
    )

    is_correct = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.username    

    