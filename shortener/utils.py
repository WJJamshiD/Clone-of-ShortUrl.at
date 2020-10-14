import random
import string
from django.conf import settings

MIN_CHARS=getattr(settings,'MIN_CHARS',5)

def generate_code(size=MIN_CHARS,chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_shortcode(instance,size=MIN_CHARS):
    Klass=instance.__class__
    shortcode=generate_code(size=size)
    used=Klass.objects.filter(shortcode=shortcode).exists()
    if used:
        shortcode=generate_shortcode(size=size)
    return shortcode
