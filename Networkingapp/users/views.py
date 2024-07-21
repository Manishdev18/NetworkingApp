from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailsSerializer, FriendRequestSerializer, FriendSerializer
from .models import FriendRequest, Friend, CustomUser



# User Refistation Api
class UserRegistrationView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                ints = serializer.save()
                return Response({'message': 'User registered successfully', 'status' :True}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
        except Exception  as e:
             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST )





class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = UserDetailsSerializer(user)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception  as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST )
        

        
class FriendRequestPendingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            friend_requests = FriendRequest.objects.filter(receiver = user, status="pending")
            friend_requests_serializer = FriendRequestSerializer(friend_requests, many= True)
            friend_requests_data = friend_requests_serializer.data
            return Response(friend_requests_data, status=status.HTTP_200_OK)

        except Exception  as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST )
        
    
        
class AcceptRejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
            try:
                data = request.data
                friend_request_id = kwargs.get('pk')
                friend_request = FriendRequest.objects.filter(id=friend_request_id, receiver=request.user, status = "pending")
                if friend_request.exists():
                    if data["status"] == "accepted":
                        friend_request =friend_request.first()
                        friend_request.status = "accepted"
                        friend_request.save()
                        Friend.objects.create(user=friend_request.sender, friend=friend_request.receiver)
                        Friend.objects.create(user=friend_request.receiver, friend=friend_request.sender)
                        return Response({'message': 'Friend Request Accepted', 'status' :True}, status=status.HTTP_200_OK)
                    elif data["status"] == "rejected":
                        friend_request.status = "rejected"
                        friend_request.save()
                        Response({'message': 'Friend Request Rejected', 'status' :True}, status=status.HTTP_200_OK)
                    return Response({'message': 'status not identified', 'status' :True}, status=status.HTTP_200_OK)


                else:
                    return Response({'message': 'Firend Request Does not Found', 'status' :False}, status=status.HTTP_200_OK)
            except Exception  as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST )
            


class ListOfFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = request.GET
            page_number = 1
            page_limit = 10

            if "page_number" in data:
                page_number = data["page_number"]
            if "page_limit" in data:
                page_limit = data['page_limit']
            friends = Friend.objects.filter(user=request.user)
            friend_paginated = Paginator(friends, page_limit)
            page_obj = friend_paginated.page(page_number)
            freind_paginated_obj = page_obj.object_list
            friends_serializer = FriendSerializer(freind_paginated_obj, many=True)
            friends_data = friends_serializer.data
            return Response({"data": friends_data, "num_pages": friend_paginated.num_pages}, status=status.HTTP_200_OK)
        except Exception  as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST )
        

        




class SendFriendRequestView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request, *args, **kwargs):
        try:
            user = request.user
            now = timezone.now()
            one_minute_range = now - timedelta(minutes=1)
            recent_requests_count = FriendRequest.objects.filter(sender=user,created_at__gte=one_minute_range).count()
            if recent_requests_count>=3:
                return Response({"message": "exceeded the limit of 3 friend requests per minute", "status": False}, status.HTTP_200_OK)
            receiver = CustomUser.objects.filter(id=kwargs.get('pk')).first()
            if receiver:
                friend_request = FriendRequest.objects.filter(sender=user, receiver= receiver).first()
                if friend_request:
                    return Response({"message": "Friend Request Already Sent", "status": False}, status.HTTP_200_OK)
                FriendRequest.objects.create(sender=user,receiver=receiver)
                return Response({"message": "Friend Request  Sent", "status": True}, status.HTTP_200_OK)
                
  
            else:
                return Response({'message': 'Reciver  Does not Found', 'status' :False}, status=status.HTTP_400_BAD_REQUEST)


        except Exception  as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST )
        

        
class SearchUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data = request.GET
            page_number = 1
            page_limit = 10

            if "page_number" in data:
                page_number = data["page_number"]
            if "page_limit" in data:
                page_limit = data['page_limit']
            query = request.query_params.get("search", None)

            if query ==None:
                return Response({"detail": "No search Key provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            if "@" in query:
                search_users = CustomUser.objects.filter(email__icontains=query)
            else:
                full_name = query.split()

                if len(full_name) ==2:
                    search_users = CustomUser.objects.filter(first_name__icontains=full_name[0], last_name__icontains=full_name[1])
                elif len(full_name) ==1:
                    search_users = CustomUser.objects.filter(first_name__icontains=full_name[0])
                else:
                    search_users = CustomUser.objects.none()
            
            user_paginated = Paginator(search_users, page_limit)
            page_obj = user_paginated.page(page_number)
            user_paginated_obj = page_obj.object_list
            user_serializer = UserDetailsSerializer(user_paginated_obj, many=True)
            user_data = user_serializer.data
            return Response({"data": user_data,  "num_pages":  user_paginated.num_pages}, status=status.HTTP_200_OK)

        except Exception  as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST )


