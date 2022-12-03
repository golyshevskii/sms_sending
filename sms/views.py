from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from .models import SendingMessages, Client, Message
from .serializers import SendingMessagesSerializer, ClientSerializer, MessageSerializer


class SendingMessagesViewSet(viewsets.ModelViewSet):
    serializer_class = SendingMessagesSerializer
    queryset = SendingMessages.objects.all()

    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        """Summary data for a specific sending message list"""

        queryset_mailing = SendingMessages.objects.all()
        get_object_or_404(queryset_mailing, pk=pk)
        queryset = Message.objects.filter(mailing_id=pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def fullinfo(self, request):
        """Summary data for all send messages"""

        total_count = SendingMessages.objects.count()
        sending_messages = SendingMessages.objects.values('id')
        content = {'Total number of sending messages': total_count,
                   'The number of messages sent': ''}
        result = {}
        
        for row in sending_messages:
            res = {'Total messages': 0, 'Sent': 0, 'No sent': 0}
            mail = Message.objects.filter(mailing_id=row['id']).all()
            group_sent = mail.filter(sending_status='Sent').count()
            group_no_sent = mail.filter(sending_status='No sent').count()
            res['Total messages'] = len(mail)
            res['Sent'] = group_sent
            res['No sent'] = group_no_sent
            result[row['id']] = res
        
        content['The number of messages sent'] = result
        return Response(content)

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

