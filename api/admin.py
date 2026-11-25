from django.contrib import admin
from .models import Question, MCQQuestion, MCQOption, Lesson


admin.site.register(Question)


class MCQOptionInline(admin.TabularInline):
    model = MCQOption
    extra = 4


@admin.register(MCQQuestion)
class MCQQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'difficulty', 'created_at')
    list_filter = ('difficulty',)
    search_fields = ('question',)
    inlines = [MCQOptionInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'order', 'is_published', 'created_at')
    list_filter = ('topic', 'is_published')
    search_fields = ('title', 'topic')
    list_editable = ('order', 'is_published')
    ordering = ('order',)