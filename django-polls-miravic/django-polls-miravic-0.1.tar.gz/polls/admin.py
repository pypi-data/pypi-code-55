from django.contrib import admin

# Register your models here.
from .models import Choice, Question

# admin.site.register(Question)

# class ChoiceInLine(admin.StackedInline):
#     model = Choice
#     extra = 3

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {"fields": ['question_text']}),
        ('Date Information', {"fields": ['pub_date']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']




# admin.site.register(Choice)

admin.site.register(Question, QuestionAdmin)