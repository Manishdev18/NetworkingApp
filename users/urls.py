from django.urls import path
from .views import UserRegistrationView, UserDetailsView,FriendRequestPendingView,AcceptRejectFriendRequestView,\
    SendFriendRequestView, ListOfFriendView, SearchUserView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
    path('pending-requests/', FriendRequestPendingView.as_view(), name='pending-friend-requests'),
    path('accept_reject-request/<int:pk>/', AcceptRejectFriendRequestView.as_view(), name='accept-reject-friend-request'),
    path('send-request/<int:pk>/', SendFriendRequestView.as_view(), name ='send-friend-request' ),
    path('friend-list', ListOfFriendView.as_view(), name="freind-list"),
    path('user-search/', SearchUserView.as_view(), name="user-list-search")
  
]
