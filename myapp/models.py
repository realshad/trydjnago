from django.db import models
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    sid = models.IntegerField(null=False)
    sname = models.CharField(max_length=120)
    dob = models.DateTimeField()

    class meta:
        db_table="student"
"""
class employees(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20, null = True)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    class Meta:
         db_table = "employees"

    def __str__(self):
        return self.first_name
"""

class employees1(models.Model):
    GENDER_TYPE_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    employee_id = models.AutoField(primary_key=True)
    emp_uid = models.CharField(unique=True, max_length=120, null=True)
    first_name = models.CharField(max_length=20, null = True)
    last_name = models.CharField(max_length=25)
    Gender = models.CharField(null=True, max_length=3, choices=GENDER_TYPE_CHOICES)
    Date_of_birth = models.DateField(blank=True, null=True)
    date_of_join = models.DateField(blank=True, null=True, default=timezone.now)
    emp_age = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=25)
    created_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=120, null=True)
    updated_by = models.CharField(max_length=120, null=True)
    class Meta:
         db_table = "employees1"
    # custom manager replaces objects manger
    all_employees = models.Manager()

    def __str__(self):
        return self.emp_uid

    @property
    def get_emp_age(self):
        import datetime
        return int(((datetime.date.today() - self.Date_of_birth).days / 365.25))

    @property
    def get_unique_id(self):
        a = self.last_name[:2].upper()  # First 2 letters of last name
        b = self.Date_of_birth.strftime('%d')  # Day of the month as string
        c = self.date_of_join.strftime('%m')  # Day of the month as string
        d = 'CMP-'
        return d + a + b + c

    def save(self, *args, **kwargs):
        self.emp_uid= self.get_unique_id
        self.emp_age = self.get_emp_age
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(employees1, self).save(*args, **kwargs) # Call the "real" save() method.

        # ABSOLUTE URL METHOD
        def get_absolute_url(self):
            return reverse('hhome', kwargs={'pk': self.id})

class departments1(models.Model):
    department_id = models.IntegerField(primary_key=True)
    department_name = models.CharField(max_length=30)
    manager = models.ForeignKey(employees1, null = True, on_delete=models.PROTECT)
    created_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=120, null=True)
    updated_by = models.CharField(max_length=120, null=True)

    class Meta:
         db_table = "departments1"

    def __int__(self):
        return self.department_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(departments1, self).save(*args, **kwargs)

class Product(models.Model):
    title		=models.CharField(max_length=120)
    description	=models.TextField(blank=True, null=True)
    price		=models.DecimalField(decimal_places=2, max_digits=10000)
    summary		=models.TextField(blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.title

    def get_absolute_url(self):
        return f"Produpdate/{self.id}"
