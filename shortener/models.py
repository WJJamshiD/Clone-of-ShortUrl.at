from django.db import models
from django.conf import settings
from .utils import generate_shortcode
from django_hosts.resolvers import reverse
from .validators import validate_url

MAX_CHARS=getattr(settings,'MAX_CHARS','10')
# Create your models here.

class WjUrlManager(models.Manager):
    def inactives(self,*args, **kwargs):
        qs=super(WjUrlManager,self).all(*args, **kwargs).filter(active=True)
        return qs

    def refresh_shortcodes(self,number=None,size=None):
        qs=WjUrl.objects.filter(id__gte=1)
        if number is not None and isinstance(number,int):
            qs=qs.order_by('-id')[:number]    
        new_codes=0
        for q in qs:
            print(q.url,'|',q.shortcode,end='|')
            if size is not None and isinstance(size,int):
                q.shortcode=generate_shortcode(instance=q,size=size)
            else:
                q.shortcode=generate_shortcode(instance=q)
            q.save()
            new_codes+=1
            print(q.shortcode,'|',new_codes)
        return 'New codes made: {}'.format(new_codes)

class WjUrl(models.Model):
    url=models.CharField(max_length=240,validators=[validate_url])
    shortcode=models.CharField(max_length=MAX_CHARS,unique=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    objects=WjUrlManager()

    def __str__(self):
        return self.url

    def save(self,*args, **kwargs):
        if self.shortcode==None or self.shortcode=='':
            self.shortcode=generate_shortcode(self)
        if not 'http' in self.url:
            self.url='http://' +self.url 
        super(WjUrl,self).save(*args,**kwargs)

    def get_short_url(self):
        url=reverse("shorten", kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
        return url

    def get_clicks_url(self):
        url=reverse("clicks", kwargs={'shortcode': self.shortcode})
        return url

class Message(models.Model):
    username=models.CharField(max_length=240,null=True,blank=True)
    email=models.EmailField()
    content=models.TextField(max_length=4000,null=False,blank=False)
    timestamp=models.DateTimeField(auto_now_add=True)
    
