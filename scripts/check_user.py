from django.contrib.auth.models import User
from clients.models import UserProfile

user = User.objects.first()
print(f'User: {user.username}')
profile = user.profile
print(f'Profile exists: {profile is not None}')
if profile and profile.home_care_office:
    print(f'Home Care Office: {profile.home_care_office.name}')
    print(f'Office Number: {profile.home_care_office.office_number}')
else:
    print('Home Care Office: Not set')
