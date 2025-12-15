from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from .utils import send_email_async


@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_email_async(
            subject='Registration Successful',
            message="""Jay Shree Ram 🙏🚩,

Your registration on Dharma AI was successful!

I’m Subhajit Kar, the developer of this application, and I personally want to thank you for joining.

You are now ready to experience AI-guided wisdom inspired by Sanatan Dharma, the wisdom of Ramayan, Bhagavad Gita, and Sunderkand.

If you have any questions or feedback, feel free to reach out anytime.

Wishing you a meaningful and blessed experience ahead 🌼
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email]
        )
