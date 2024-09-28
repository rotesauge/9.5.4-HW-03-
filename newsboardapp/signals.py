from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post
from django.template.loader import render_to_string
from django.core.mail import send_mail,mail_managers
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f' post created {instance.caption} {instance.author}'
    else:
        subject = f'post created {instance.caption} {instance.author}'

    html_content = render_to_string(
        'post_created.html',
        {
            'post': instance,
        }
    )
    tolist = []
    categs =  instance.сategory.all()
    for categ in categs:
        subs = categ.subscribers.all()
        for sub in subs:
            tolist.append(sub.email)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=instance.text,
        from_email='rotesauge@aiq.ru',
        to=tolist,
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем

    mail_managers(
        subject=subject,
        message=instance.message,
    )