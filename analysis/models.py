from django.db import models
from shortener.models import WjUrl
# Create your models here.



class ClickEventManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, WjUrl):
            obj, created = self.get_or_create(url=instance)
            obj.number += 1
            obj.save()
            return obj.number
        return None


class ClickEvent(models.Model):
    url=models.OneToOneField(WjUrl,on_delete=models.CASCADE)
    number=models.PositiveIntegerField(default=0)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    objects=ClickEventManager()

    def __str__(self):
        return str(self.number)