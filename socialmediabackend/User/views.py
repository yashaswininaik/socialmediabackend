from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, FriendRequest
from .serializers import UserCreateSerializer, UserViewSerializer, TokenObtainPairSerializer, FriendRequestSerializer
from .utils import UserRateThrottleByMinute


class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserCreateSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class FriendListView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user

        # Retrieve all the records where the current user is either sender or receiver
        friends = User.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__status='accepted') |
            Q(received_requests__from_user=user, received_requests__status='accepted')
        ).distinct()

        # Serialize the friend objects
        serializer = UserViewSerializer(friends, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class SearchFriendList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        search_query = self.request.query_params.get('search_query', '')
        search_type = self.request.query_params.get('search_type', 'name')  # Default to 'name' if not provided

        if not search_query:
            return Response({"error": "Search query is required"}, status=HTTP_400_BAD_REQUEST)

        queryset = User.objects.exclude(pk=self.request.user.pk)

        if search_type == 'email':
            queryset = queryset.filter(email__iexact=search_query)
        else:
            queryset = queryset.filter(first_name__icontains=search_query)

        serializer = UserViewSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SendFriendRequest(APIView):

    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottleByMinute,)

    def post(self, request, to_user_id):
        from_user = request.user
        to_user = get_object_or_404(User, pk=to_user_id)

        # Check if the request is already sent
        existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
        if existing_request.exists():
            return Response({"error": "Friend request already sent"}, status=HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=HTTP_201_CREATED)


class RespondToFriendRequest(APIView):

    permission_classes = (IsAuthenticated,)

    def put(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, pk=request_id)
        if friend_request.to_user != request.user:
            return Response({"error": "You are not authorized to respond to this request"}, status=HTTP_403_FORBIDDEN)

        status_param = request.data.get('status')
        if status_param not in ['accepted', 'rejected']:
            return Response({"error": "Invalid status"}, status=HTTP_400_BAD_REQUEST)

        friend_request.status = status_param
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data)
