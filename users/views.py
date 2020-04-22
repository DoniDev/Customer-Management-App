from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout

from accounts.models import Customer
from users.decorators import unauthenticated_user,allowed_users

@unauthenticated_user
def register(request):
    # if request.user.is_authenticated:
    #     #     return redirect('home')
    #     # else:
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(
            #     user=user,
            #     name=user.username,
            #     email=email,
            # )
            messages.success(request, f'Account was created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form':form,
    }
    return render(request,'users/register.html',context=context)




@unauthenticated_user
def auth_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request,'Username or Password is incorrect')
    return render(request,'users/login.html')


def auth_logout(request):
    logout(request)
    return redirect('login')


@allowed_users(['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context={
        'orders': orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
    }
    return render(request,'users/user.html',context=context)