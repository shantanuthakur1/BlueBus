from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book, Route
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
import datetime

def home(request):
    context={}
    if request.user.is_authenticated:
        context['uuser'] = request.user.name
        return render(request, 'myapp/home.html', context)
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        seats_r = request.POST.get('seats')
        price_r = request.POST.get('price')

        hrs_r = request.POST.get('h')
        if hrs_r:
            hrs_r = int(hrs_r)
        else:
            hrs_r = 0
        mins_r = request.POST.get('m')
        if mins_r:
            mins_r = int(mins_r)
        else:
            mins_r = 0

        route_list = Route.objects.filter(source__icontains=source_r, dest__icontains=dest_r)
        if not route_list:
            context["error"] = "Sorry no buses availiable from "+source_r+" to "+dest_r
            return render(request, 'myapp/findbus.html', context)
        route_id_list=[]
        for x in route_list:
            route_id_list.append(x.route_id)      
        bus_list = Bus.objects.filter(r_id__in=route_id_list ,  date=date_r)
        if not bus_list:
            context["error"] = "Sorry no buses availiable from "+source_r+" to "+dest_r+" on "+date_r
            return render(request, 'myapp/findbus.html', context)
        if(seats_r):
            bus_list=bus_list.filter(rem__gte=int(seats_r))
            if not bus_list:
                context["error"] = "Sorry no buses availiable with " + seats_r + " free seats"
                return render(request, 'myapp/findbus.html', context)
        if(price_r):
            bus_list=bus_list.filter(price__lte=int(price_r))         
            if not bus_list:
                context["error"] = "Sorry no buses availiable with a ticket price lower than "+price_r
                return render(request, 'myapp/findbus.html', context)
        if(hrs_r or mins_r ):
            bus_list=bus_list.filter(r_id__duration__lte=datetime.timedelta(hours=hrs_r, minutes=mins_r))
            if not bus_list:
                context["error"] = "Sorry no buses availiable with a journey duration less than "+str(hrs_r)+" hours and "+str(mins_r)+" minutes."
                return render(request, 'myapp/findbus.html', context)
        return render(request, 'myapp/list.html', locals())
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def book(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        try:
            bus = Bus.objects.get(bus_id=id_r)
        except Bus.DoesNotExist:
            bus = None
        if bus:
            if bus.rem >= int(seats_r):
                bus.rem = bus.rem - seats_r
                bus.save()
                booking = Book.objects.create(user_id=request.user, bus_id=bus, no_seats=seats_r)
                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry. You are trying to book too many seats."
                return render(request, 'myapp/findbus.html', context)
        else:
            context["error"]="You entered an invalid bus id!"
            return render(request, 'myapp/findbus.html',context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        try:
            booking = Book.objects.get(booking_id=request.POST.get('bk_id'))
            if request.user == booking.user_id:
                if not booking.status:
                    context["error"] = "This booking is already cancelled"
                    return seebookings(request,context)
                booking.bus_id.rem = booking.bus_id.rem + booking.no_seats
                booking.status=False
                booking.bus_id.save()
                booking.save()
                context["error"] = "Cancelled successfully!"
                return seebookings(request,context)
            else:
                context["error"] = "You can only cancel a booking of your own!"
                return seebookings(request,context)
        except Book.DoesNotExist:
            context["error"] = "Please select a valid booking id"
            return seebookings(request,context)
    else:
        return render(request, 'myapp/findbus.html')

@login_required(login_url='signin')
def seebookings(request, new={}):
    context={}
    booking_list = Book.objects.filter(user_id=request.user)
    if booking_list:
        if new:
            error = new["error"]
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no bookings found"
        return render(request, 'myapp/findbus.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('findbus')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            return redirect(home)
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "Login failed"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)
