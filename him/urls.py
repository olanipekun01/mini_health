from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    # path('auth/register/', views.register_user, name='register'),
   
    
    # Patients (HIM only)
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    
    # Case Folders (HIM only for creation, HIM/Doctor for viewing)
    path('casefolders/', views.CaseFolderListCreateView.as_view(), name='casefolder-list-create'),
    path('casefolders/<int:pk>/', views.CaseFolderDetailView.as_view(), name='casefolder-detail'),
    
    # Medical History (Doctors only)
    path('casefolders/<int:case_folder_id>/medical-history/', views.MedicalHistoryListCreateView.as_view(), name='medical-history-list-create'),
    
    # Diagnoses (Doctors only)
    path('casefolders/<int:case_folder_id>/diagnoses/', views.DiagnosisAdmissionListCreateView.as_view(), name='diagnosis-list-create'),
    
    # Vital Signs (Nurses only)
    path('casefolders/<int:case_folder_id>/vitals/', views.VitalSignsListCreateView.as_view(), name='vitals-list-create'),
    
    # Patient Notes (Nurses and Doctors)
    path('casefolders/<int:case_folder_id>/notes/', views.PatientNoteListCreateView.as_view(), name='notes-list-create'),
]
