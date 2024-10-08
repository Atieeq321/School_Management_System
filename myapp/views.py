from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from myapp.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.models import CustomUser


def Index(request):
    return render(request, 'index.html')

def Base(request):
    return render(request, 'base.html')

def Login(request):
    return render(request, 'login.html')

def DoLogin(request):
    if request.method=="POST":
        user=EmailBackEnd.authenticate(request,
                                        username=request.POST.get('email'),
                                        password = request.POST.get('password'))
        if user != None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect("hod_home")
            elif user_type == '2':
                return HttpResponse("<h1> This is Staff Panal </h1>")
            elif user_type == '3':
                return HttpResponse("<h1> This is Student Panal </h1>")
            else:
                messages.error(request, "Email and Password are incorrect")
                return redirect('login')
        else:
            messages.error(request, "Email and Password are incorrect")
            return redirect('login')
   

def DoLogout(request):
    logout(request)
    return redirect("login")

@login_required(login_url='/')
def Profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user" : user,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
def Profile_Update(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # u_name = request.POST.get('username')
        password = request.POST.get('password')
        #print(profile_pic, f_name, l_name, password)

        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            if profile_pic != None and profile_pic != "":  
                customuser.profile_pic = profile_pic
            #customuser.profile_pic = profile_pic
            customuser.first_name = first_name
            customuser.last_name = last_name
            # customuser.email = email
            # customuser.username = u_name    
            if password != None and password != "":  
                customuser.set_password(password)  
            customuser.save()      
            messages.success(request, "Your Profile Updated Successfully")
            return redirect("profile")

        except:
            messages.error(request, "Profile Updation Failed")
    return render(request, "profile.html")




