from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from .models import SendingMessages, Client, Message
from .tasks import send_message


@receiver(post_save, sender=SendingMessages, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        sm = SendingMessages.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(Q(mobile_operator_code=sm.mobile_operator_code) | Q(tag=sm.tag)).all()
        
        for client in clients:
            Message.objects.create(
                sending_status="No sent",
                client_id=client.id,
                mailing_id=instance.id
            )
            message = Message.objects.filter(mailing_id=instance.id, client_id=client.id).first()
            data = {
                'id': message.id,
                "phone": client.phone_number,
                "text": sm.text
            }
            client_id = client.id
            sm_id = sm.id
            
            if instance.to_send:
                send_message.apply_async((data, client_id, sm_id), expires=sm.date_end)
            else:
                send_message.apply_async((data, client_id, sm_id), eta=sm.date_start, expires=sm.date_end)
