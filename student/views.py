from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from master.models import Book, Account
from master.forms import RegistrationForm

# Create your views here.


@login_required(login_url = 'student-login')
def student_home(request):
    book = Book.objects.all()
    context = {
        'book' : book,
    }
    return render(request, 'student/student.html', context)




#student registration
def student_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password,
                phone_number = phone_number,
            )
            
            user.save()
            
            messages.success(request,'Registration is successfull')
            return redirect('student-login')            
            
    else:
        form = RegistrationForm()

    context = {
        'form' : form,
    }
    return render(request,'student/student_registration.html', context)   



#student Login
def student_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email = email , password = password)
        if user is not None:
            
                auth.login(request,user)
                messages.success(request, "You are logged in")
                return redirect('student-home')
            
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('student-login')
    return render(request, 'student/student_login.html')



#student logout
@login_required(login_url = 'student-login')
def student_logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('student-login')


