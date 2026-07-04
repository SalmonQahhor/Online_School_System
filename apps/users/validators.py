import re
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
 

 
def validate_email_format(email):
    """Professional email regex validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('Email formati noto\'g\'ri. Misol: user@example.com')
 
 
def validate_password_strength(password):
    """Strong password validation"""
    if len(password) < 8:
        raise ValidationError('Parol kamida 8 belgi bo\'lishi kerak.')
    
    if not any(c.isupper() for c in password):
        raise ValidationError('Parolda kamida 1 ta katta harf bo\'lishi kerak.')
    
    if not any(c.islower() for c in password):
        raise ValidationError('Parolda kamida 1 ta kichik harf bo\'lishi kerak.')
    
    if not any(c.isdigit() for c in password):
        raise ValidationError('Parolda kamida 1 ta raqam bo\'lishi kerak.')
    
    if not any(c in '!@#$%^&*-_=+' for c in password):
        raise ValidationError('Parolda kamida 1 ta special belgi bo\'lishi kerak (!@#$%^&*-_=+)')
    
    # Common passwords
    common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein']
    if password.lower() in common_passwords:
        raise ValidationError('Bu parol juda oddiy. Boshqasini tanlang.')
 
 
def validate_grade(grade):
    """Grade validation (0-100)"""
    if grade is None:
        return
    
    if not isinstance(grade, int):
        raise ValidationError('Ball butun son bo\'lishi kerak.')
    
    if not 0 <= grade <= 100:
        raise ValidationError('Ball 0 dan 100 gacha bo\'lishi kerak.')
 
 
def validate_file_upload(file):
    """File upload validation - size, type"""
    if not isinstance(file, UploadedFile):
        return
    
    # Max 15MB
    max_size = 15 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError(f'Fayl hajmi 15MB dan oshmasligi kerak. Hozir: {file.size / (1024*1024):.2f}MB')
    
    # Allowed file types
    allowed_extensions = ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar']
    file_ext = file.name.split('.')[-1].lower()
    
    if file_ext not in allowed_extensions:
        raise ValidationError(f'Fayl turi qo\'planmagan. Ruxsat etilgan: {", ".join(allowed_extensions)}')
 
 
def validate_username(username):
    """Username validation"""
    if len(username) < 3:
        raise ValidationError('Username kamida 3 belgi bo\'lishi kerak.')
    
    if len(username) > 30:
        raise ValidationError('Username 30 belgidan oshmasligi kerak.')
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError('Username faqat harf, raqam, _ va - belgilarini o\'z ichiga olishi mumkin.')
