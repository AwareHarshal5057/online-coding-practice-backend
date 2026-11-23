from django.contrib import admin
from .models import Question
from .models import MCQQuestion,MCQOption

admin.site.register(Question)

class MCQOptionInline(admin.TabularInline):
    model = MCQOption
    extra = 4

@admin.register(MCQQuestion)
class MCQQuestionAdmin(admin.ModelAdmin):
    list_display = ('id','question','difficulty','created_at')
    list_filter = ('difficulty',)
    search_fields = ('question',)
    inlines = [MCQOptionInline]


