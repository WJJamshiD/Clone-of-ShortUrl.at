from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.contrib.messages import add_message,ERROR,SUCCESS
from .models import WjUrl
from django.views import View
from django.http import Http404,HttpResponseRedirect
from analysis.models import ClickEvent
from .forms import SubmitUrlForm,MessageForm,CounterForm
import random

# Create your views here.

class HomeView(View):
    def get(self,request,*args, **kwargs):
        form = SubmitUrlForm()
        return render(request, 'home.html',{'form':form})
   
    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "form": form,
        }
        template = "home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = WjUrl.objects.get_or_create(url=new_url)
            if created:
                template = "success.html"
            else:
                add_message(request,ERROR,'It was shortened before, use this:') 
                template = "success.html"
            context = {
                "object": obj,
            }
        else:
            add_message(request,ERROR,'Please enter a valid URL.')
        return render(request, template ,context)



class UrlRedirectView(View):
    def get(self,request,shortcode,*args, **kwargs):
        obj=get_object_or_404(WjUrl,shortcode=shortcode)
        ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj.url)


class CounterView(View):
    def get(self,request,*args, **kwargs):
        form = CounterForm()
        return render(request, 'counter.html',{'form':form})
   
    def post(self, request, *args, **kwargs):
        form = CounterForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get("url")
            try:
                if url[:8]=='https://':
                    url=url[8:]
                if url[:7]=='http://':
                    url=url[7:]
                if url[:4]=='www.':
                    url=url[4:]
                shortcode=url[15:]
                if shortcode[-1]=='/':
                    shortcode=shortcode[:-1]
            except:
                add_message(request,ERROR,'Please see examples below.')
                return render(request, 'counter.html', {'form':form})
            obj= WjUrl.objects.filter(shortcode=shortcode)
            if obj.exists():
                obj=obj.first()
                return redirect("clicks", shortcode=obj.shortcode)
            else:
                add_message(request,ERROR,'It seems this url is not shortened yet!')
        else:
            add_message(request,ERROR,'Please enter a valid URL.')
        return render(request, 'counter.html', {'form':form})

class ClicksView(View):
    def get(self,request,shortcode,*args, **kwargs):
        obj=get_object_or_404(WjUrl,shortcode=shortcode)
        return render(request,'click_counts.html',{'object':obj})




MathQuizs={'17-4':13,
            '5*9':45,
            '47+2':49,
            '12-7':5,
            '3+9':12,
            '4*7':28}


class ContactView(View):
    def get(self,request,*args, **kwargs):
        mathquiz=random.choice(list(MathQuizs.keys()))
        math1=MathQuizs[mathquiz]
        form = MessageForm()
        context={
            'math1':math1,
            'mathquiz':mathquiz,
            'form':form
        }
        return render(request, 'contact.html',context)
   
    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            add_message(request,SUCCESS,'Your message sent succesfully.')
            return redirect('contact')
        mathquiz=random.choice(list(MathQuizs.keys()))
        math1=MathQuizs[mathquiz]
        context={
        'math1':math1,
        'mathquiz':mathquiz,
        'form':form
        }
        
        return render(request, 'contact.html', context)

