from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, BookForm
from .models import Account, Book
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator

# Create your views here.


@login_required(login_url = 'master-login')
def masterHome(request):
    book_count= Book.objects.count()
    student = Account.objects.filter(is_superadmin=False)
    student_count = student.count()
    context = {
        'book_count':book_count,
        'student_count' : student_count,

    }
    return render(request, 'master/master.html', context)

 

#Admin registration
def master_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_superuser(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password,
                phone_number = phone_number,
            )
            
            user.save()
            
            messages.success(request,'Registration is successfull')
            return redirect('master-login')            
            
    else:
        form = RegistrationForm()

    context = {
        'form' : form,
    }
    return render(request,'master/master_registration.html', context)   



#Admin Login
def master_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email = email , password = password,is_superadmin=True)
        if user is not None:
            if user.is_superadmin:
                auth.login(request,user)
                request.session['admin']=email
                messages.success(request, "You are logged in")
                return redirect('master-home')
            else:
                messages.error(request, 'you are not a Master')
                return redirect('master-login')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('master-login')
    return render(request, 'master/login.html')



#Admin logout
@login_required(login_url = 'login')
def master_logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('master-login')



#Add books
@login_required(login_url = 'master-login')
def add_book(request):
    form = (BookForm)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('book_list')
        else:
            messages.warning(request, 'enter correct details')

    context = {
        'form' : form,
    }               

    return render(request,'master/add_book.html', context)


#update a book record
@login_required(login_url = 'master-login')
def edit_book(request,id):
    book = Book.objects.get(id=id)
    form = BookForm(instance=book)
    if request.method=='POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')

    context = {
        'form' : form,
        'book' : book,
    }        
    return render(request, 'master/edit_book.html', context)



#delete a book record
@login_required(login_url = 'master-login')
def delete_book(request,id):
    book = Book.objects.filter(id=id)
    book.delete()
    return redirect('book_list')


#book list - to view all the books
@login_required(login_url = 'master-login')
def book_list(request):
    book = Book.objects.all()
    
    #pagination
    paginator = Paginator(book, 10)
    page = request.GET.get('page')
    pageed_products = paginator.get_page(page)

    context = {
        'book' : pageed_products,
    }

    return render(request, 'master/book_list.html', context)



#student list
@login_required(login_url = 'master-login')
def student_list(request):
    student = Account.objects.filter(is_superadmin=False)

    #pagination
    paginator = Paginator(student, 10)
    page = request.GET.get('page')
    pageed_products = paginator.get_page(page)

    context = {
        'student':pageed_products,
    }
    return render(request,'master/student_list.html',context)


def block_unblock_student(request, id):
    user = Account.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, 'user is Blocked Successfully')
    else:
        user.is_active = True
        messages.success(request, 'user is un Blocked Successfully')

    user.save()
    return redirect('student-list')    


    
