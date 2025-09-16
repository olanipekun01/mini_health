from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, CaseFolder, MedicalHistory, DiagnosisAdmission, VitalSigns, PatientNote

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active',)
#     list_filter = ('role', 'is_active', 'is_staff',)
#     # fieldsets = BaseUserAdmin.fieldsets + (
#     #     ('Role Information', {'fields': ('role', 'phone')}),
#     # )
#     # add_fieldsets = BaseUserAdmin.add_fieldsets + (
#     #     ('Role Information', {'fields': ('role', 'phone')}),
#     #     ('Authorization', {'fields': ('is_authorized')}),
#     # )

admin.site.register(User)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'dob', 'gender', 'phone', 'created_by', 'created_at')
    list_filter = ('gender', 'created_at', 'created_by')
    search_fields = ('first_name', 'last_name', 'phone', 'email')

@admin.register(CaseFolder)
class CaseFolderAdmin(admin.ModelAdmin):
    list_display = ('folder_number', 'patient', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('folder_number', 'patient__first_name', 'patient__last_name')

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('case_folder', 'hypertension', 'diabetes', 'tb', 'created_at')
    list_filter = ('hypertension', 'diabetes', 'tb', 'measles', 'chicken_pox')

@admin.register(DiagnosisAdmission)
class DiagnosisAdmissionAdmin(admin.ModelAdmin):
    list_display = ('case_folder', 'date', 'date_of_admission', 'date_of_discharge', 'created_by')
    list_filter = ('date', 'date_of_admission', 'created_by')
    search_fields = ('case_folder__patient__first_name', 'case_folder__patient__last_name', 'diagnosis')

@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ('case_folder', 'blood_pressure', 'pulse', 'weight', 'recorded_by', 'recorded_at')
    list_filter = ('recorded_at', 'recorded_by')

@admin.register(PatientNote)
class PatientNoteAdmin(admin.ModelAdmin):
    list_display = ('case_folder', 'date', 'user_type', 'recorded_by', 'created_at')
    list_filter = ('user_type', 'date', 'created_at')
    search_fields = ('surname', 'other_names', 'notes')
