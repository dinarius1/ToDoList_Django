from django.urls import path
from .views import SendFriendRequestView, RespondFriendRequestView, ListFriendRequestsView, RetrieveFriendRequestView #ListFriendsView

urlpatterns = [
    path('friend_request/', SendFriendRequestView.as_view()),
    path('respond_friend_request/<int:request_id>/', RespondFriendRequestView.as_view(), name='respond_friend_request'),
    path('friend_requests/', ListFriendRequestsView.as_view(), name='list_friend_requests'),
    # path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('friend_requests/<int:request_id>/', RetrieveFriendRequestView.as_view(), name='retrieve_friend_request'),
]
