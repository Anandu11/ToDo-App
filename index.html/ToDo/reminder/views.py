from django.shortcuts import render,redirect
from django.views.generic import View
from reminder.forms import register,signin,TaskForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from reminder.models import Task
from django.utils.decorators import method_decorator

#Create your views here.


def signin_required(fn):   
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper    


def mylogin(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Task.objects.get(id=id)
        if obj.user != request.user:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,mylogin]    
# @method_decorator(decs,name='dispatch')         

class Signup(View):
    def get(self,request,*args,**kwargs):
        form=register()
        return render(request,"rem.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=register(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            User.objects.create_user(**form.cleaned_data)
        form=register()    
        return render(request,"rem.html",{"form":form})

class Sigin(View):
    def get(self,request,*args,**kwargs):
        form=signin()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=signin(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                login(request,user_obj)
                print("valid credentials")
                return redirect("task")
            else:
                print("invalid credentials")  
               
        return render(request,"login.html",{"form":form})
        




           
@method_decorator(signin_required,name='dispatch')
class Taskview(View):
      def get(self,request,*args,**kwargs):
          form=TaskForm()
          data=Task.objects.filter(user=request.user).order_by('completion')
          return render(request,"index.html",{"form":form,"data":data})
          


      def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST) 
        if form.is_valid():
            form.instance.user=request.user
            form.save()
        data=Task.objects.filter(user=request.user)    
        return render(request,"index.html",{"form":form,"data":data})    

class Taskupdate(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Task.objects.get(id=id)
        if obj.completion == False:
            obj.completion = True
            obj.save()
        else:
            obj.completion = False
            obj.save()

        return redirect("task")

@method_decorator(mylogin,name='dispatch')
class Taskdelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.filter(id=id).delete()
        return redirect("task")

class signout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")
    

class user_del(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        User.objects.filter(id=id).delete()
        return redirect("rem")
