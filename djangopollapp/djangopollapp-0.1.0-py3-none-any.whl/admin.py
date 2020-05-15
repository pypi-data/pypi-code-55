from django.contrib import admin
from .models import Polls, Questions, TextAnswer, Choices, ClientsID


class ChoiceInline(admin.TabularInline):
    model = Choices
    exclude = ['votes']
    extra = 4


class TextAnswerInline(admin.TabularInline):
    model = TextAnswer
    exclude = ['votes']
    extra = 4


class QuestionsInline(admin.TabularInline):
    model = Questions
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class PollsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'title', 'description', 'members']}),
        ('Date info', {'fields': ['start_date', 'end_date']}),
    ]
    readonly_fields = ['start_date']
    inlines = [QuestionsInline]


class ClientsIDAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Guest', {'fields': ['unique_id', 'date_create']}),
    ]
    readonly_fields = ['unique_id', 'date_create']
    list_display = ['unique_id', 'date_create']


admin.site.register(Polls, PollsAdmin)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(TextAnswer)
admin.site.register(Choices)
admin.site.register(ClientsID, ClientsIDAdmin)
