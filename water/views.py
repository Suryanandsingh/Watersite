from django.contrib.auth import (
    login, logout,get_user_model,
    )
from django.http import HttpResponseRedirect #for return particular page
from django.shortcuts import render, redirect #for go to html page
from .models import Brand, ZipCode, Quality
from django.db.models import Q  #for query search
from .form import LoginForm,  MyRegistrationForm , UserProfileForm, EditProfile#for login or RegisterForm
from django.contrib.auth.decorators import login_required #for log in require
from django.contrib.auth.forms import UserChangeForm

User=get_user_model()

#for home page
def index(request):
    all_brand = Brand.objects.all() #all object
    query = request.GET.get("q")#query for search
    if query: #filter query search
        all_brand = all_brand.filter(
            Q(brand__icontains=query))#| Q(size__contains=query) |Q(price__contains=query)
    #return page of index and all_brand  is dict for all above object
    return render(request, 'water/index.html', {'all_brand': all_brand,})



#for detail of each brand

def detail(request, brand_id):
    brandDe = Brand.objects.get(pk=brand_id)#get thought id in brandDe
    #return details page
    
    pin = ZipCode.objects.all()

    #price = Quality.objects.all()
    #pname = request.POST['dropdown1']
    #print(pname)
    '''if request.POST: 
        quality = Quality.objects.get(pname=pname)
        print(quality)'''

    args = {'details': brandDe , 'pin':pin}

    return render(request, 'water/detail.html', args)


#for login
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('/water')# Redirect to a success page.
    return render(request, 'water/form.html', {'form': form })



#for registration
def Register_View(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('/water/login')
    else:
        form = MyRegistrationForm()

    return render(request, 'water/registration_form.html', {'form':form})


@login_required(login_url='/water/login/') #check if user login or not if not then go to login page
# @transaction.atomic
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/water')
    else:
        user = request.user
        form = UserProfileForm(instance=request.user.profile)

    return render(request, 'water/profile.html', {'form':form})


#logout
def Pincode(request):
    pin = ZipCode.objects.all()
    return render(request, 'water/pin.html', {'pin':pin})





def account(request):
    # user = UserProfileForm.objects.all()
    # args = {'user':user}
    if request.method =='POST':
        form = UserProfileForm(request.POST)
        print(form.cleaned_data['address'])
        # print(user.profile.address)
    return render(request, 'water/user_profile_details.html')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/water/account/')
    else:
        form = EditProfile(instance=request.user)
        return render(request, 'water/edit_profile.html', {"form":form})


def logoutView(request):
    logout(request)
    return redirect("/water/")
