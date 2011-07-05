from django.core.mail.message import EmailMessage
from django.core.management.base import BaseCommand
from smtplib import SMTPException
from subscribe.models import MailTask
import settings

class Command(BaseCommand):
    def handle(self, *args, **optionals):
        for m_task in MailTask.objects.filter(sent=MailTask.STATUS_IN_PROGRESS):
            try:
                msg = EmailMessage(subject=m_task.title,
                                   body=m_task.message,
                                   from_email=settings.SERVICE_EMAIL_ADDRESS,
                                   to=[m_task.subscribe.email])
                msg.content_subtype = 'html'
                msg.send()
                m_task.sent = MailTask.STATUS_OK

            except SMTPException as e:
                m_task.sent = MailTask.STATUS_PROVIDER_FAILURE
                m_task.exception_message = str(e)
            except Exception as e:
                m_task.sent = MailTask.STATUS_INNER_FAILURE
                m_task.exception_message = str(e)
            finally:
                m_task.save()