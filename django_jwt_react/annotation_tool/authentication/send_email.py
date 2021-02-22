import os
from pathlib import Path
from email.mime.image import MIMEImage
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
class EmailAlert():
    sender="no-reply@ellogon.gr"
    image_path = '/home/alex/PycharmProjects/django_jwt_react/django_jwt_react/annotation_tool/frontend/static/frontend/images/EllogonCyan.png'
    def __init__(self,recipient,username,content):
        self.username=username
        self.recipient=recipient
        self.image_name = Path(EmailAlert.image_path).name
        self.content=content

    def send_activation_email(self):
        subject="Account Activation"
        text_message = f"This is an automatic email from {EmailAlert.sender}.Please don't reply"
        cwd=os.path.abspath(os.getcwd())
        template_path=os.path.abspath(os.path.join(cwd, os.pardir))+"/annotation_tool/frontend/templates/frontend/activation.html"

        html_message=get_template(template_path).render(self.content)
        html_message = str(html_message).format(image_name=self.image_name)
        text_message=text_message+"\n"+html_message
      #  print(message)
        msg = EmailMultiAlternatives(subject=subject, body=text_message, from_email=EmailAlert.sender,to=[self.recipient])
        msg.attach_alternative(html_message, "text/html")
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        with open(EmailAlert.image_path, mode='rb') as f:
            image = MIMEImage(f.read())
            msg.attach(image)
            image.add_header('Content-ID', f"<{self.image_name}>")
        msg.send()
        #send_mail(subject,body,EmailAlert.sender,[self.recipient])
    def send_resetpassword_email(self):
        subject="Reset Password"
        text_message = f"This is an automatic email from {EmailAlert.sender}.Please don't reply"
        cwd=os.path.abspath(os.getcwd())
        template_path=os.path.abspath(os.path.join(cwd, os.pardir))+"/annotation_tool/frontend/templates/frontend/reset_password.html"
        html_message = get_template(template_path).render(self.content)
       # print("pass2:" + self.content["password"])
        html_message = str(html_message).format(image_name=self.image_name)
      #  print(message)
        text_message = text_message + "\n" + html_message
        msg = EmailMultiAlternatives(subject=subject, body=text_message, from_email=EmailAlert.sender,to=[self.recipient])
        msg.attach_alternative(html_message, "text/html")
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        with open(EmailAlert.image_path, mode='rb') as f:
            image = MIMEImage(f.read())
            msg.attach(image)
            image.add_header('Content-ID', f"<{self.image_name}>")
        msg.send()