from django.conf import settings
from django.http import HttpResponseRedirect

DEFAULT_REDIRECT_URL=getattr(settings,'DEFAULT_REDIRECT_URL','http://www.wjurl.com')


def wildcard_redirect(request,path=None):
    print(path)
    url=DEFAULT_REDIRECT_URL
    print(url)
    if path:
        url=DEFAULT_REDIRECT_URL+'/'+path
    print(url)
    return HttpResponseRedirect(url)