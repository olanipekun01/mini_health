from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Patient, CaseFolder, MedicalHistory, DiagnosisAdmission, VitalSigns, PatientNote
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.crypto import get_random_string


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'password', 'password_confirm', 'is_superuser', 'is_staff',)
    
    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password_confirm']:
    #         raise serializers.ValidationError("Passwords don't match")
    #     return attrs

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages
            )
        return attrs
    
    # def create(self, validated_data):
    #     validated_data.pop('password_confirm')
    #     user = User.objects.create_user(**validated_data)
    #     return user
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            # date_of_birth=validated_data['date_of_birth'],
            # gender=validated_data['gender'],
            role=validated_data['role'],
            phone=validated_data['phone'],
            is_superuser=validated_data['is_superuser'],
            is_staff=validated_data['is_staff']
        )
        # use set_password method to hash the password
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return user.tokens
    
    class Meta:
        model = User
        fields = ['password', 'username', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if not User.objects.filter(username=username).exists():
            raise AuthenticationFailed('Invalid username, try again')
        
        user = auth.authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid password, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        if not user.is_authorized:
            raise AuthenticationFailed('Your account has not been approved by an admin')

        serializer = UserSerializer(user)
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens(),
            'user': serializer.data,
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            # self.fail('bad_token')
            raise serializers.ValidationError(str(e))


# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         user = User.objects.filter(email=value).first()
#         if user is None:
#             raise serializers.ValidationError("No user found with this email address.")
#         return value

#     def save(self):
#         email = self.validated_data['email']
#         user = User.objects.get(email=email)
#         otp = get_random_string(length=6, allowed_chars='1234567890')
#         user.login_token = otp
#         user.save()
#         return {'user': user, 'otp': otp}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'created_at']

class PatientSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'dob', 'gender', 'matric_no', 'jamb_no', 'address', 'phone', 'email', 'xray_no', 'religion', 'state_of_origin', 'tribe', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['id', 'hypertension', 'measles', 'chicken_pox', 'tb', 'diabetes', 'liver_disease', 'sti',
         'yellow_fever', 'liver_disease', 'epilepsy', 'sc_disease', 'gd_ulcer', 'rta_injury', 'alcohol_smoking',
         'previous_ops', 'schistosomiasis', 'respiratory_disease', 'mental_disease', 'hiv', 'allergies', 'recorded_by',
          'created_at', 'updated_at']

class DiagnosisAdmissionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = DiagnosisAdmission
        fields = ['id', 'date', 'diagnosis', 'date_of_admission', 'date_of_discharge', 'recorded_by', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

class VitalSignsSerializer(serializers.ModelSerializer):
    recorded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = VitalSigns
        fields = ['id', 'blood_pressure', 'pulse', 'weight', 'height', 'urine_albumin', 'urine_sugar', 'recorded_by', 'recorded_at']
        read_only_fields = ['recorded_by', 'recorded_at']

class PatientNoteSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True)
    
    class Meta:
        model = PatientNote
        fields = ['id', 'surname', 'other_names', 'date', 'notes', 'user_type', 'recorded_by', 'created_at']
        read_only_fields = ['profile', 'created_at']

class CaseFolderSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    medical_history = MedicalHistorySerializer(read_only=True)
    diagnoses = DiagnosisAdmissionSerializer(many=True, read_only=True)
    vital_signs = VitalSignsSerializer(many=True, read_only=True)
    notes = PatientNoteSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = CaseFolder
        fields = ['id', 'patient', 'patient_id', 'folder_number', 'medical_history', 'diagnoses', 'vital_signs', 'notes', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
