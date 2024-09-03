from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import EmailTokenObtainPairView, RegisterView, FriendListView, SearchFriendList, SendFriendRequest, RespondToFriendRequest
#url patthers
urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('login/', EmailTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friend-list/', FriendListView.as_view(), name='friend_list'),
    path('search-friends/', SearchFriendList.as_view(), name='search_friend'),
    path('send-friend-request/<int:to_user_id>/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('respond-friend-request/<int:request_id>/', RespondToFriendRequest.as_view(), name='respond_to_friend_request'),
]