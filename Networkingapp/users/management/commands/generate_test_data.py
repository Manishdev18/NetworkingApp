# users/management/commands/generate_test_data.py

from django.core.management.base import BaseCommand
from users.models import CustomUser, FriendRequest, Friend

class Command(BaseCommand):
    help = 'Create test data for CustomUser, FriendRequest, and Friend models'

    def handle(self, *args, **kwargs):
        # Create test users
        users = []
        for i in range(1, 11):
            user = CustomUser.objects.create_user(
                email=f'user{i}@example.com', 
                password='password123', 
                first_name=f'User{i}', 
                last_name=f'Last{i}'
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))

        # Create friend requests and friends
        for i in range(0, len(users) - 1):
            sender = users[i]
            receiver = users[i + 1]

            # Create friend request
            friend_request = FriendRequest.objects.create(
                sender=sender, 
                receiver=receiver, 
                status='accepted'
            )
            self.stdout.write(self.style.SUCCESS(f'Created friend request from {sender.email} to {receiver.email}'))

            # Create friend relationship
            Friend.objects.create(user=sender, friend=receiver)
            self.stdout.write(self.style.SUCCESS(f'Created friendship between {sender.email} and {receiver.email}'))

        # Creating additional friend requests that are not accepted
        for i in range(0, len(users) - 2, 2):
            sender = users[i]
            receiver = users[i + 2]

            # Create friend request with pending status
            FriendRequest.objects.create(
                sender=sender, 
                receiver=receiver, 
                status='pending'
            )
            self.stdout.write(self.style.SUCCESS(f'Created pending friend request from {sender.email} to {receiver.email}'))

        self.stdout.write(self.style.SUCCESS('Test data creation complete.'))
