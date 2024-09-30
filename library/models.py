from ast import expr
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime ,timedelta

class Book(models.Model):
    name=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    isbn=models.PositiveIntegerField()
    category=models.CharField(max_length=50)
    
    def __str__(self):
       return str(self.name) + "["+str(self.isbn)+']'
    
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    classroom=models.CharField(max_length=20)
    branch=models.CharField(max_length=10)
    roll_no=models.IntegerField(blank=False)
    phone=models.IntegerField(blank=True)
    image=models.ImageField(upload_to="/media",null=True,blank=True)
    
    def __str__(self):
        return str(self.user)+"["+str(self.branch)+']'+"["+str(self.classroom)+']'+"["+str(self.roll_no)+']'
    
def expiry():
    return datetime.today() + timedelta(days=30)
class IssuedBook(models.Model):
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13)
    issued_date=models.DateField(auto_now=True)
    expiry_date=models.DateField(default=expiry)
    
    
        
