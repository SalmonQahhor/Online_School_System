# Online School System — API Guide


## Base URL
http://127.0.0.1:8000/api/v1/auth/


## 1. Invite (Admin only)
POST /invite/
Headers: Authorization: Bearer <admin_token>
Body: { "email": "teacher@test.com", "role": "teacher" }
Response: { "message": "Invite yuborildi." }


## 2. Validate Token
GET /invite/validate/?token=UUID
Response: { "email": "teacher@test.com", "role": "teacher" }


## 3. Register
POST /register/
Body: { "token": "UUID", "username": "teacher1", "password": "pass1234" }
Response: { "message": "Ro'yxatdan o'tdingiz..." }


## 4. Login
POST /login/
Body: { "email": "teacher@test.com", "password": "pass1234" }
Response: {
"access": "eyJ...",
"refresh": "eyJ...",
"role": "teacher",
"email": "teacher@test.com"
}


## 5. Me (Current User)
GET /me/
Headers: Authorization: Bearer <access_token>
Response: { "email": "...", "username": "...", "role": "teacher", ... }


## 6. Profile Edit
GET /profile/
Headers: Authorization: Bearer <access_token>
Response: { "email": "...", "username": "...", ... }
PATCH /profile/
Headers: Authorization: Bearer <access_token>
Body: { "username": "new_name", "first_name": "Ali" }
Response: { "message": "Profil yangilandi.", "user": {...} }


## 7. Change Password
POST /change-password/
Headers: Authorization: Bearer <access_token>
Body: {
"old_password": "pass1234",
"new_password": "newpass5678",
"confirm_password": "newpass5678"
}
Response: { "message": "Parol muvaffaqiyatli o'zgartirildi." }


## 8. Logout
POST /logout/
Headers: Authorization: Bearer <access_token>
Body: { "refresh": "eyJ..." }
Response: { "message": "Muvaffaqiyatli chiqildi." }


## 9. Token Refresh
POST /token/refresh/
Body: { "refresh": "eyJ..." }
Response: { "access": "eyJ..." }
