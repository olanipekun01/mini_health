from rest_framework.permissions import BasePermission

class IsHIMRole(BasePermission):
    """Permission class for HIM role"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'HIM'

class IsNurseRole(BasePermission):
    """Permission class for Nurse role"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'NURSE'

class IsDoctorRole(BasePermission):
    """Permission class for Doctor role"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'DOCTOR'

class IsPharmacyRole(BasePermission):
    """Permission class for Pharmacy role"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'PHARMACY'

class IsHIMOrDoctorRole(BasePermission):
    """Permission class for HIM or Doctor roles"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['HIM', 'DOCTOR']

class IsNurseOrDoctorRole(BasePermission):
    """Permission class for Nurse or Doctor roles"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['NURSE', 'DOCTOR']


class IsHIMNurseOrDoctorRole(BasePermission):
    """Permission class for HIM or Doctor roles"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['HIM', 'NURSE', 'DOCTOR']