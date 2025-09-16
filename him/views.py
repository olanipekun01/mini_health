from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from app.models import User, Patient, CaseFolder, MedicalHistory, DiagnosisAdmission, VitalSigns, PatientNote
from app.serializers import (
    RegisterSerializer, PatientSerializer, CaseFolderSerializer,
    MedicalHistorySerializer, DiagnosisAdmissionSerializer, VitalSignsSerializer, PatientNoteSerializer
)
from app.permissions import IsHIMRole, IsNurseRole, IsDoctorRole, IsHIMOrDoctorRole, IsNurseOrDoctorRole, IsHIMNurseOrDoctorRole


# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def register_user(request):
#     """Register a new user with role"""
#     serializer = UserRegistrationSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'message': 'User registered successfully',
#             'user': {
#                 'id': user.id,
#                 'username': user.username,
#                 'role': user.role,
#             },
#             'tokens': {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
#         }, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Patient Views (HIM Only)
class PatientListCreateView(generics.ListCreateAPIView):
    """List and create patients - HIM role only"""
    serializer_class = PatientSerializer
    permission_classes = [IsHIMRole]
    
    def get_queryset(self):
        return Patient.objects.all()

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete patient - HIM role only"""
    serializer_class = PatientSerializer
    permission_classes = [IsHIMRole]
    queryset = Patient.objects.all()

# Case Folder Views
class CaseFolderListCreateView(generics.ListCreateAPIView):
    """List and create case folders - HIM role only"""
    serializer_class = CaseFolderSerializer
    permission_classes = [IsHIMRole]
    
    def get_queryset(self):
        return CaseFolder.objects.all()

class CaseFolderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete case folder - HIM or assigned doctor only"""
    serializer_class = CaseFolderSerializer
    permission_classes = [IsHIMOrDoctorRole]
    queryset = CaseFolder.objects.all()

# Medical History Views
class MedicalHistoryListCreateView(generics.ListCreateAPIView):
    """List and create medical history - Doctors only"""
    serializer_class = MedicalHistorySerializer
    permission_classes = [IsNurseOrDoctorRole]
    
    def get_queryset(self):
        case_folder_id = self.kwargs.get('case_folder_id')
        return MedicalHistory.objects.filter(case_folder_id=case_folder_id)
    
    def perform_create(self, serializer):
        case_folder_id = self.kwargs.get('case_folder_id')
        case_folder = get_object_or_404(CaseFolder, id=case_folder_id)
        serializer.save(case_folder=case_folder)

# Diagnosis Views
class DiagnosisAdmissionListCreateView(generics.ListCreateAPIView):
    """List and create diagnoses - Doctors only"""
    serializer_class = DiagnosisAdmissionSerializer
    permission_classes = [IsNurseOrDoctorRole]
    
    def get_queryset(self):
        case_folder_id = self.kwargs.get('case_folder_id')
        return DiagnosisAdmission.objects.filter(case_folder_id=case_folder_id)
    
    def perform_create(self, serializer):
        case_folder_id = self.kwargs.get('case_folder_id')
        case_folder = get_object_or_404(CaseFolder, id=case_folder_id)
        serializer.save(case_folder=case_folder, created_by=self.request.user)

# Vital Signs Views
class VitalSignsListCreateView(generics.ListCreateAPIView):
    """List and create vital signs - Nurses only"""
    serializer_class = VitalSignsSerializer
    permission_classes = [IsNurseOrDoctorRole]
    
    def get_queryset(self):
        case_folder_id = self.kwargs.get('case_folder_id')
        return VitalSigns.objects.filter(case_folder_id=case_folder_id)
    
    def perform_create(self, serializer):
        case_folder_id = self.kwargs.get('case_folder_id')
        case_folder = get_object_or_404(CaseFolder, id=case_folder_id)
        serializer.save(case_folder=case_folder, recorded_by=self.request.user)

# Patient Notes Views
class PatientNoteListCreateView(generics.ListCreateAPIView):
    """List and create patient notes - Nurses and Doctors"""
    serializer_class = PatientNoteSerializer
    permission_classes = [IsNurseOrDoctorRole]
    
    def get_queryset(self):
        case_folder_id = self.kwargs.get('case_folder_id')
        return PatientNote.objects.filter(case_folder_id=case_folder_id)
    
    def perform_create(self, serializer):
        case_folder_id = self.kwargs.get('case_folder_id')
        case_folder = get_object_or_404(CaseFolder, id=case_folder_id)
        user_type = 'DOCTOR' if self.request.user.role == 'DOCTOR' else 'NURSE'
        serializer.save(case_folder=case_folder, profile=self.request.user, user_type=user_type)
