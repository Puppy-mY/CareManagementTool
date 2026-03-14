from django.contrib.auth.models import User
from clients.models import UserProfile, HomeCareSupportOffice

# adminユーザーを取得
user = User.objects.get(username='admin')
profile = user.profile

# 安濃津ろまんを取得
office = HomeCareSupportOffice.objects.filter(name__contains='安濃津ろまん').first()

if office:
    profile.home_care_office = office
    profile.save()
    print(f'設定完了: {user.username} の所属事業所を「{office.name}」に設定しました')
    print(f'事業所番号: {office.office_number}')
    print(f'住所: {office.address}')
else:
    print('安濃津ろまんが見つかりませんでした')
