import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


def create_users():
    users = [
        ('adminuser', 'Admin', 'User', 'mypassword', 'myuser@mymail.com'),
    ]
    for username, first, last, password, email in users:
        try:
            print('Creating user {0}.'.format(username))
            user, created = User.objects.update_or_create(
                username=username,
                defaults={
                    'is_staff': True,
                    'is_superuser': True,
                    'first_name': first,
                    'last_name': last,
                    "email": email
                }
            )
            if created:
                user.set_password(password)
                user.save()
                assert authenticate(username=username, password=password)
                print('User {0} successfully created.'.format(username))
            else:
                print('User {0} successfully updated.'.format(username))

        except:
            print('There was a problem creating the user: {0}.  Error: {1}.'.format(username, sys.exc_info()[1]))
