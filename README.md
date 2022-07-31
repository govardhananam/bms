# Booking Management

Run
pip install -r requirements.txt and install dependencies required.

Configure Mailers in settings.py(app)

Modify Google API and Azure AD keys.

Configure AWS s3 for media storage.

Two views:

Teacher and Student

Single login page for both- Authenticated using Django inbuilt Groups

Custom Authentication Model with Password reset capability.

Configured for Heroku Deployment.


Django Rest Framework based API's.

visit /api for the list of api's available

Used to book labs and sessions enables teacher to release solts and students to book them.

Upon successful booking student will receive an email confirming booking.


Postgres Setup:

Create a postgres db

and update the creds in settings.py

and create django superuser

to register go to register_student/ or register_teacher/ for student and admin access respectively.

Add course and Unit through django in built admin panel.

You can add procedures in custom built admin panel.

Upon adding those parameters you will have access to publish booking through custom admin panel.




https://user-images.githubusercontent.com/24703858/182013802-f48e0f88-61cd-4a35-9a67-113fb5e94ddf.mp4




