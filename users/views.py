from rest_framework import generics
from rest_framework.permissions import AllowAny

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, BalanceTopUpSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class TopUpBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BalanceTopUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        user = request.user
        user.balance += amount
        user.save(update_fields=["balance"])

        return Response(
            {"balance":user.balance},
            status=status.HTTP_200_OK
        )