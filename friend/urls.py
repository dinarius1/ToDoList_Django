from django.urls import path
from .views import RequestFriendListCreateView, RequestFriendRetrieveUpdateDestroyView, ReceivedFriendRequestsListView, RespondFriendRequestView, FriendUserRetrieveUpdateDestroyView, FriendListView, FollowedTaskListView #FriendsListView, FriendsRetrieveUpdateDestroyView


urlpatterns = [
    path('friend_list/', FriendListView.as_view()),
    path('followed_task/', FollowedTaskListView.as_view()),
    path('friend_user/<int:pk>', FriendUserRetrieveUpdateDestroyView.as_view()),
    path('request/', RequestFriendListCreateView.as_view()),
    path('request/<int:pk>', RequestFriendRetrieveUpdateDestroyView.as_view()),
    path('received_friend_request/', ReceivedFriendRequestsListView.as_view()),
    path('respond_friend_request/<int:pk>/', RespondFriendRequestView.as_view()),
]
