#!/usr/bin/env python
import os
import django
import sys

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(__file__))

# Django設定を読み込み
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from django.contrib.auth.models import User

# スーパーユーザーを作成
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"スーパーユーザー '{username}' を作成しました")
    print(f"ユーザー名: {username}")
    print(f"パスワード: {password}")
else:
    print(f"ユーザー '{username}' は既に存在します")