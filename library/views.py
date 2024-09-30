from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate,login,logout
from . import forms,models
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
    return render(request,"index.html")

@login_required(login_url='/admin_login')
def add_book(request):
    if request.method=="POST":
        name=request.POST['name']
        author=request.POST['author']
        isbn=request.POST['isbn']
        category=request.POST['category']
        
        books =Book.objects.create(name=name,author=author,isbn=isbn,category=category)
        books.save()
        alert=True
        return render(request,"add_book.html",{'alert':alert})
    return render(request,"add_book.html")

@login_required(login_url='/admin_login')
def view_books(request):
    books=Book.objects.all()
    return render(request,"view_books.html",{'books':books})

@login_required(login_url='/admin_login')
def view_students(request):
    students=Student.objects.all()
    return render(request,"view_students.html",{'students':students})

@login_required(login_url='/admin_login')
def issue_book(request):
   if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect upon successful form submission
   else:
        form = IssueBookForm()  # Blank form for GET request
    
   return render(request, 'issue_book.html', {'form': form})  
    
    
    # form =IssueBookForm()
    # if request.method=="POST":
    #     form= IssueBookForm(request.POST)
    #     if form.is_valid():
    #         obj =models.IssuedBook()
    #         obj.student_id=request.POST['name2']
    #         obj.isbn=request.POST['isbn2']
    #         obj.save()
    #         alert=True
    #         return render(request,"issue_book.html",{'obj':obj,'alert':alert})
    #     return render(request,"issue_book.html",{'form':form})
    

@login_required(login_url='/admin_login')
def view_issued_book(request):
    issuedBooks = models.IssuedBook.objects.all()
    details=[]
    for i in issuedBooks:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>30:
            day=d-30
            fine=day*5
        books=list(models.Book.objects.filter(isbn=i.isbn))
        students=list(models.Student.ojects.filter(user=i.student_id))
      
        for book,student in zip(books,students):
            t=(student.user,student.user_id,book.name,book.isbn,i.expiry_date,fine)
            
            details.append(t)
    return render(request,"view_issued_book.html",{'issuedBooks':issuedBooks,'details':details})

@login_required(login_url='/admin_login')
def student_issued_books(request):
    student =Student.objects.filter(user_id=request.user.id)
    issuedBooks=models.IssuedBook.objects.filter(student_id=student[0].user_id)
    li1=[]
    li2=[]
    
    for i in issuedBooks:
        books= Book.objects.filter(isbn=i.isbn)
        for book in books:
            t=(request.user.id,request.user.get_full_name,book.name,book.author)
            li1.append(t)
        
        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>31:
            day=d-30
            fine=day*5
            t=(issuedBooks[0].issued_date,issuedBooks[0].expiry_date,fine)
            li2.append(t)
    return render(request,'student_issued_books.html',{'li1':li1,'li2':li2})
        
@login_required(login_url = '/student_login')
def profile(request):
    return render(request,"profile.html")

@login_required(login_url = '/student_login')
def edit_profile(request):
    student=Student.objects.filter(user=request.user).first()
    
    if student is None:
         return render(request, 'edit_profile.html', {'error': 'Student profile not found.'})
    if request.method=="POST":
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        branch = request.POST.get('branch')
        roll_no = request.POST.get('roll_no')
        classroom = request.POST.get('classroom')
        
        student.user.email=email
        student.phone=phone
        student.branch=branch
        student.classroom=classroom
        student.roll_no=roll_no
        student.user.save()
        student.save()
        alert=True
        
        return render(request,'edit_profile.html',{'alert':alert}) 
    return render(request,"edit_profile.html")

def delete_book(request,myid):
    books=Book.objects.filter(id=myid)
    books.delete()
    return redirect("/views_books")

def delete_student(request,myid):
    students= Student.objects.filter(id=myid)
    students.delete()
    return redirect("/view_students")

def change_password(request):
    if request.method=="POST":
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        try:
            u =User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert=True
                return render(request,"change_password.html",{'alert':alert})
            else:
                currpasswrong= True
                return render(request,"change_password.html",{'currpasswrong':currpasswrong})
        except:
            pass
    return render(request,"change_password.html")

def student_registration(request):
    if request.method =='POST':
       username = request.POST.get('username')
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       email = request.POST.get('email')
       phone = request.POST.get('phone')
       branch = request.POST.get('branch')
       classroom = request.POST.get('classroom')
       roll_no = request.POST.get('roll_no')
       image = request.FILES.get('image')
       password = request.POST.get('password')
       confirm_password = request.POST.get('confirm_password')
       
       if not first_name or not last_name:
            return render(request, 'student_registration.html', {'error': 'First and last name are required.'})
       
       if User.objects.filter(username=username).exists():
            return render(request, 'student_registration.html', {'error': 'Username already taken.'})
       
       if password !=confirm_password:
           passnotmatch=True
           return render(request,"student_registration.html",{'passnotmatch':passnotmatch})
       
       user= User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name) 
       student= Student.objects.create(user=user,phone=phone,branch=branch,classroom=classroom,roll_no=roll_no)
       return redirect('/student_login')
    #    user.save()
       #student.save()
#  alert=True
    #    return (request,"student_registration.html",{'alert':alert})
    return render(request,"student_registration.html")


def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert})
    return render(request, "student_login.html")

    # if request.method == 'POST':
    #     username = request.POST('username')
    #     password = request.POST('password')

    #     # Authenticate user
    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         return redirect('/profile')  # Redirect to student dashboard
    #     else:
    #         # Pass 'alert' variable to template to show error message
    #         return render(request, 'student_login.html', {'alert': True})

    # # Render the login page on GET request
    # return render(request, 'student_login.html')
  
    
    
    # alert=False
    # if request.method=="POST":
    #     username= request.POST['username']
    #     password=request.POST['password']
    #     user=authenticate(username=username,password=password)
        
    #     print(f"username:{username},password:{password}")
    #     if user is not None:
    #         if user.is_active:
    #          login(request,user)
    #          if request.user.is_superuser:
    #             return HttpResponse("you are not a student!!")
    #          else:
    #             return redirect("/profile")
    #         else:
    #          alert=True
    #     else:
    #       alert=True        
    #     return render(request,"student_login.html",{'alert':alert})
    # return render(request,"student_login.html")
            
def admin_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
          
        if user is not None:
              login(request, user) 
              if request.user.is_superuser:
                  return redirect("/add_book") 
              else:
                  return HttpResponse("you are not admin.")
        else:
            alert=True
            return render(request,"admin_login.html",{'alert':alert})
    return render(request,"admin_login.html") 

def user_logout(request):
     logout(request)
     return redirect("/")
              