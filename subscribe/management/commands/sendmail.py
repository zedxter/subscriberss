from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from smtplib import SMTPException
from subscribe.models import MailTask
import settings

class Command(BaseCommand):
    def handle(self, *args, **optionals):
        for m_task in MailTask.objects.filter(sent=MailTask.STATUS_IN_PROGRESS):
            try:
                send_mail(subject=m_task.title,
                          message=m_task.message,
                          from_email=settings.SERVICE_EMAIL_ADDRESS,
                          recipient_list=[m_task.subscribe.email])
                m_task.sent = MailTask.STATUS_OK

            except SMTPException:
                m_task.sent = MailTask.STATUS_PROVIDER_FAILURE
            except Exception:
                m_task.sent = MailTask.STATUS_INNER_FAILURE
            finally:
                m_task.save()