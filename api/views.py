from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from .models import KBEntry
from .serializers import KBEntrySerializer
from rest_framework.permissions import AllowAny
from .models import KBEntry, QueryLog

from .serializers import QuerySerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .authentication import APIKeyAuthentication
from .serializers import QueryLogSerializer
from .authentication import APIKeyAuthentication
from django.db.models import Q

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )

            user.company.company_name = serializer.validated_data["company_name"]
            user.company.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "User registered successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "api_key": user.company.api_key,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email
        })

class KBEntryListCreateView(generics.ListCreateAPIView):
    queryset = KBEntry.objects.all()
    serializer_class = KBEntrySerializer
    permission_classes = [IsAuthenticated]


class KBEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KBEntry.objects.all()
    serializer_class = KBEntrySerializer
    permission_classes = [IsAuthenticated]


class KBQueryView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuerySerializer(data=request.data)

        if serializer.is_valid():
            question = serializer.validated_data["question"]

            entry = KBEntry.objects.filter(
            Q(question__icontains=question) |
            Q(answer__icontains=question) |
            Q(category__icontains=question)
            ).first()

            if entry:
                answer = entry.answer
            else:
                answer = "No matching answer found."

            QueryLog.objects.create(
                company=request.user.company,
                question=question,
                response=answer
            )

            return Response({
                "question": question,
                "answer": answer
            })

        return Response(serializer.errors, status=400)

class LoginView(TokenObtainPairView):
    pass

class QueryHistoryView(generics.ListAPIView):
    serializer_class = QueryLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QueryLog.objects.filter(
            company=self.request.user.company
        ).order_by("-created_at")