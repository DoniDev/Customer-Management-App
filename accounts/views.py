
from django.shortcuts import render, redirect

from accounts.filters import OrderFilter
from accounts.forms import OrderForm, CustomerForm
from accounts.models import Product, Customer, Order
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users,admin_only

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-date_created')

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        'customers':customers,
        'orders':orders,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
    }
    return render(request,'accounts/dashboard.html',context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {}
    context['products'] = products
    return render(request, 'accounts/products.html',context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()

    all_order = Order.objects.all()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'myFilter':myFilter,
        'all_order':all_order,
    }
    return render(request, 'accounts/customer.html',context=context)




#CRUD
# def createOrder(request, pk):
#     OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
#     customer = Customer.objects.get(id=pk)
#     formset = OrderFormSet( queryset=Order.objects.none(),instance=customer)
#     # form = OrderForm(initial={'customer':customer})
#     if request.method == 'POST':
#         formset = OrderFormSet(request.POST,instance=customer)
#         if formset.is_valid():
#             formset.save()
#             return redirect('home')
#     # else:
#     #     formset = OrderFormSet(instance=customer)
#     context=  {
#         'form': formset,
#     }
#     return render(request,'accounts/order_form.html',context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST,initial={'customer':customer})
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrderForm(initial={'customer':customer})
    context={
        'form':form,
    }
    return render(request,'accounts/order_form.html',context=context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(request.POST, instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrderForm(instance=order)
    context = {
        'form':form,
    }
    return render(request,'accounts/order_form.html',context=context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context = {
        'item':order,
    }
    return render(request,'accounts/delete.html',context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accounts_settings(request):
    customer  = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()



    context={'form':form}
    return render(request,'accounts/accounts_settings.html',context=context)



