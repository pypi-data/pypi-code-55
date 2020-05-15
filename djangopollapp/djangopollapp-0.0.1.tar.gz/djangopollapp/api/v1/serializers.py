from rest_framework import serializers
from djangopollapp.models import Polls, Questions, TextAnswer, Choices, ClientsID


class TextAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextAnswer
        fields = (
            'id',
            'qns',
            'text',
            'author',
        )


class ChoicesSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField('is_selected')

    def is_selected(self, obj):
        if 'request' in self.context and 'client_id' in self.context['request'].COOKIES:
            client = ClientsID.objects.get(unique_id=self.context['request'].COOKIES['client_id'])
            if client in obj.votes.all():
                return True
            else:
                return False
        else:
            return None

    class Meta:
        model = Choices
        fields = (
            'id',
            'qns',
            'text',
            'vote_counter',
            'selected',
        )


class QuestionSerializer(serializers.ModelSerializer):
    # choices = ChoicesSerializer(many=True, required=False)
    choices = serializers.SerializerMethodField('get_choices', required=False)

    def get_choices(self, obj):
        if obj.qns_type == 1:
            if 'request' in self.context and 'client_id' in self.context['request'].COOKIES:
                try:
                    txt_ans = TextAnswer.objects.get(qns=obj,
                                                     author__unique_id=self.context['request'].COOKIES['client_id'])
                    return TextAnswerSerializer(txt_ans).data
                except:
                    return None
            else:
                return None
        else:
            return ChoicesSerializer(Choices.objects.filter(qns=obj), many=True, context=self.context).data

    class Meta:
        model = Questions
        fields = (
            'id',
            'poll',
            'qns',
            'qns_type',
            'choices',
        )

    extra_kwargs = {'choices': {'read_only': True, 'required': False}}


class PollSerializer(serializers.ModelSerializer):

    questions = serializers.SerializerMethodField('get_questions')

    def get_questions(self, obj):
        if self.context['action'] != 'list':
            qns = Questions.objects.filter(poll=obj.id)
            return QuestionSerializer(qns, many=True, context={'request': self.context['request']}).data
        else:
            return None

    class Meta:
        model = Polls
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'end_date',
            'description',
            'is_active',
            'questions'
        )
        extra_kwargs = {'start_date': {'read_only': True}, 'is_active': {'read_only': True}}