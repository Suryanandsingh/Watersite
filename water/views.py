from django.contrib.auth import (
    login, logout,get_user_model,
    )
from django.http import HttpResponseRedirect #for return particular page
from django.shortcuts import render, redirect #for go to html page
from .models import Brand, ZipCode, Quality
from django.db.models import Q  #for query search
from .form import LoginForm,  MyRegistrationForm , UserProfileForm#for login or RegisterForm
from django.contrib.auth.decorators import login_required #for log in require


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
            return HttpResponseRedirect('/water')# Redirect to a success page.
    return render(request, 'water/form.html', {'form': form })



#for registration
def Register_View(request):

        if request.method == 'POST': #for post data
            form = MyRegistrationForm(request.POST) #your post data into tha form
            if form.is_valid(): #validation your data
                form.save() #save data
                register_success = "Account successfully created!"
            return HttpResponseRedirect('/water/login')#return your index page directly
        else:
            form = MyRegistrationForm()  # An unbound form
        #return registration form with the dict form
        return render(request, 'water/registration_form.html', {'form':form})

#user profile information
@login_required(login_url='/water/login/') #check if user login or not if not then go to login page
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/water')
    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)

    return render(request, 'water/profile.html', {'form':form})


#logout
def Pincode(request):
    pin = ZipCode.objects.all()
    return render(request, 'water/pin.html', {'pin':pin})







def logoutView(request):
    logout(request)
    return redirect("/water")
