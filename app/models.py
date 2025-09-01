from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
import uuid
from django.utils.timezone import now

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('nurse', 'nurse'),
        ('doctor', 'doctor'),
        ('him', 'him'),
        ('pharm', 'pharm'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        """Check the password against the stored hashed password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.stream})"

class College(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.name

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.name

class Programme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    duration = models.IntegerField(blank=True, null=True)
    degree = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return self.name
    
class Level(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=80)

    def __str__(self):
        return self.name

class Semester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=80)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Patient(models.Model):
    STUDENTSTATUS_CHOICES = (
        ('inprogress', 'In Progress'),
        ('failed', 'Failed'),
        ('graduated', 'Graduated'),
    )

    GENDER_CHOICES = (
        ('f', 'Female'),
        ('m', 'Male'),
    )

    otherNames = models.CharField(blank=True, null=True, max_length=80)
    surname = models.CharField(blank=True, null=True, max_length=80)
    currentLevel = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='currentLevel', null=True, default=1)
    matricNumber = models.CharField(blank=True, null=True, max_length=30)
    jambNumber = models.CharField(blank=True, null=True, max_length=30)
    dateOfBirth = models.DateField()
    gender = models.CharField(blank=True, null=True, max_length=15, choices=GENDER_CHOICES)
    PhoneNumber = models.CharField(blank=True, null=True, max_length=15)
    # college = models.ForeignKey(College, on_delete=models.CASCADE, null=True)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    # programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    # entrySession = models.CharField(blank=True, null=True, max_length=15,)
    # currentSemester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, related_name='current_students')
    # ... (keep other fields as is)
    primaryEmail = models.CharField(blank=True, null=True, max_length=120)
    studentEmail = models.CharField(blank=True, null=True, max_length=120)
    bloodGroup = models.CharField(blank=True, null=True, max_length=20)
    genoType = models.CharField(blank=True, null=True, max_length=20)
    modeOfEntry = models.CharField(blank=True, null=True, max_length=50)
    entryLevel =  models.ForeignKey(Level, on_delete=models.CASCADE,  null=True, default=1)
    degree = models.CharField(blank=True, null=True, max_length=50)
    nationality = models.CharField(blank=True, null=True, max_length=110)
    stateOfOrigin = models.CharField(blank=True, null=True, max_length=110)
    localGovtArea = models.CharField(blank=True, null=True, max_length=110)
    passport = models.ImageField('image', default='images/placeholder.png', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STUDENTSTATUS_CHOICES, default='inprogress')

    def __str__(self):
        return f"{self.surname} - {self.matricNumber} (Stream A)"

class CaseFolder(models.Model):
    STATUS_CHOICES = (
        ('open ', 'open'),
        ('close', 'close'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient' null=True)
    status = models.CharField(blank=True, null=True, max_length=50, choices=STATUS_CHOICES)


    def __str__(self):
        return f"Disbursement #{self.id} by {self.user_name}"
    
class VitalsHistory(models.Model):
    casefolder = models.ForeignKey(CaseFolder, on_delete=models.CASCADE, related_name='vitalhistory' null=True)

class Consultaion(models.Model):
    casefolder = models.ForeignKey(CaseFolder, on_delete=models.CASCADE, related_name='consultation' null=True)
    complaint = models.CharField(blank=True, null=True, max_length=110)
    diagnosis = models.CharField(blank=True, null=True, max_length=110)
    plan = models.CharField(blank=True, null=True, max_length=110)