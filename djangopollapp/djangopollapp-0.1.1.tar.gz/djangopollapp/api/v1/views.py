from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from djangopollapp.models import Polls, Questions, Choices, ClientsID, TextAnswer
from djangopollapp.api.v1.serializers import PollSerializer, QuestionSerializer, TextAnswerSerializer, ChoicesSerializer


class PollView(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    serializer_class = PollSerializer

    def get_queryset(self):
        query = Polls.objects.all()
        if self.action == 'list':
            polls_list = [p.pk for p in Polls.objects.all() if p.is_active is True]
            query = Polls.objects.filter(pk__in=polls_list).order_by('-id')
            return query
        if self.action == 'retrive':
            query = Polls.objects.all()
        return query

    def get_serializer_context(self):
        return {
            'request': self.request,
            'action': self.action,
            'format': self.format_kwarg,
            'view': self
        }

    def create(self, request, *args, **kwargs):
        print(request.data.get('poll'))
        poll_data = {
            'author': request.user.id,
            **request.data.get('poll')
        }
        serializer = self.serializer_class(data=poll_data, context=self.get_serializer_context())
        try:
            serializer.is_valid(raise_exception=True)
            poll = serializer.save()

            # Check questions in data, create and adding to the poll
            if 'questions' in request.data:
                for q in request.data['questions']:
                    qns = Questions.objects.create(
                        poll=poll,
                        qns=q['qns'],
                        qns_type=q['qns_type']
                    )
                    # Check choices in data, create and adding to the questions
                    if 'choices' in q:
                        for c in q['choices']:
                            choice = Choices.objects.create(
                                qns=qns,
                                text=c['text']
                            )
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(e)
            return Response()

    @action(detail=False, url_path='for-client')
    def for_client(self, request, *args, **kwargs):
        if 'client_id' in request.COOKIES:
            polls = Polls.objects.filter(members__unique_id=request.COOKIES.get('client_id'))
            serializer = self.serializer_class(
                polls,
                many=True,
                context={
                    'request': self.request,
                    'action': self.action,
                    'format': self.format_kwarg,
                    'view': self
                }
            )
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, url_path='to-answer', methods=['post'])
    def to_answer(self, request, *args, **kwargs):
        if 'client_id' in request.COOKIES:
            client = ClientsID.objects.get(unique_id=request.COOKIES.get('client_id'))
            for q in request.data:
                question = Questions.objects.get(id=q['id'])
                if q['qns_type'] == 1:
                    choice = TextAnswer.objects.create(
                            qns=question,
                            text=q['choices'].get('text'),
                            author=client,
                        )
                elif q['qns_type'] == 2:
                    choice = Choices.objects.get(id=q['choices'])
                    choice.votes.add(client)
                elif q['qns_type'] == 3:
                    for c in q['choices']:
                        choice = Choices.objects.get(id=c)
                        choice.votes.add(client)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {
            'request': self.request,
            'action': self.action,
            'format': self.format_kwarg,
            'view': self
        }
