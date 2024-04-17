from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.utils import timezone
from datetime import datetime, timedelta
# Create your views here.
@login_required(login_url='/login')
def Home(request):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Query the database for expenses within this week
    expenses_this_week = Expense.objects.filter(transaction_date__gte=start_of_week, transaction_date__lte=end_of_week)

    # Prepare data for the chart
    clcxValues = [expense.transaction_date.strftime('%Y-%m-%d') for expense in expenses_this_week]
    clcyValues = [float(expense.amount) for expense in expenses_this_week]

    # Pass data to the template
    context = {
        'clcxValues': clcxValues,
        'clcyValues': clcyValues,
    }
    return render(request,'dashboard.html', context)

def loginpage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            print(username,password)
            return render(request, "login.html", {"error_message": "Invalid credentials"})
    else:
        return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, 'signup.html', {'error_message': error_message})

        if User.objects.filter(email=email).exists():
            error_message = "Email is already taken."
            return render(request, 'signup.html', {'error_message': error_message})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'signup.html')

@login_required(login_url='/login')
def acclogout(request):
    return redirect('login')

@login_required(login_url='/login')
def editprofile(request):
    return render(request,'editprofile.html')

@login_required(login_url='/login')
def expenses(request):
    expenses = Expense.objects.filter(user=request.user)  # Fetch expenses for the current user
    return render(request, 'expenses.html', {'expenses': expenses})

@login_required(login_url='/login')
def add_expense(request):
    if request.method == 'POST':
        transaction_date = request.POST.get('date')
        amount = request.POST.get('amount')
        is_credit_str = request.POST.get('is_credit')

        # Convert is_credit to a boolean
        is_credit = is_credit_str.lower() == 'true'

        # Create and save the Expense object
        expense = Expense(
            user=request.user,
            transaction_date=transaction_date,
            amount=amount,
            is_credit=is_credit
        )
        expense.save()

        return redirect('expenses')  # Redirect to the expenses page after adding the expense

    return render(request, 'add_expense.html')