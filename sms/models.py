import pytz
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class SendingMessages(models.Model):
    date_start = models.DateTimeField(verbose_name='Start Date')
    date_end = models.DateTimeField(verbose_name='End Date')
    time_start = models.TimeField(verbose_name='Start Time')
    time_end = models.TimeField(verbose_name='End Time')
    text = models.TextField(max_length=1000, verbose_name='Message Text')
    tag = models.CharField(max_length=100, verbose_name='Search Tags', blank=True)
    mobile_operator_code = models.CharField(verbose_name='Mobile Operator Code', max_length=3, blank=True)

    class Meta:
        verbose_name = 'Sending Message'
        verbose_name_plural = 'Sending Messages'   

    @property
    def to_send(self):
        now = timezone.now()
        if self.date_start <= now <= self.date_end:
            return True
        else:
            return False

    def __str__(self):
        return f'Sending message {self.id} from {self.date_start}'

    
class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    
    phone_regex = RegexValidator(regex=r'^7\d{10}$', message="The client's phone number in the format 7XXXXXXXXXX (X - number from 0 to 9)")
    phone_number = models.CharField(verbose_name='Phone Number', validators=[phone_regex], unique=True, max_length=11)
    mobile_operator_code = models.CharField(verbose_name='Mobile Operator Code', max_length=3, editable=False)
    tag = models.CharField(verbose_name='Search Tags', max_length=100, blank=True)
    time_zone = models.CharField(verbose_name='Time Zone', max_length=32, choices=TIMEZONES, default='UTC')
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
   
    def save(self, *args, **kwargs):
        self.mobile_operator_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'Client {self.id} with number {self.phone_number}'


class Message(models.Model):
    SENT = "sent"
    NO_SENT = "no sent"
    
    STATUS_CHOICES = [
        (SENT, "Sent"),
        (NO_SENT, "No sent"),
    ]
    
    created_time = models.DateTimeField(verbose_name='Created Time', auto_now_add=True)
    sending_status = models.CharField(verbose_name='Sending status', max_length=15, choices=STATUS_CHOICES)
    sending_messages = models.ForeignKey(SendingMessages, on_delete=models.CASCADE, related_name='sending_messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sending_messages')
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self):
        return f'Message {self.id} with text {self.sending_messages} for {self.client}'

