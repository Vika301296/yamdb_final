from api.permissions import IsAdminCustomUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .models import CustomUser
from .serializers import (ConfirmationCodeSerializer, ConfirmationSerializer,
                          CustomUserPATCHSerializer, CustomUserSerializer)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def get_confirmation_code(request):
    serializer = ConfirmationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "email": ["некорректно заполнено"],
                "username": ["некорректно заполнено"]
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = CustomUser.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email']
        )
    except Exception as error:
        return Response(
            {'Ошибка': str(error)},
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user[0])
    send_mail(
        'Confirmation code for YaMDb',
        f'Your confirmation code: {confirmation_code}',
        f'{DEFAULT_FROM_EMAIL}',
        [f'{request.data["email"]}'],
        fail_silently=False,
    )
    return Response(request.data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def get_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    user = get_object_or_404(CustomUser, username=username)
    code = request.data.get('confirmation_code')
    if default_token_generator.check_token(user, code):
        user.save()
        token = AccessToken.for_user(user)
        return Response(
            {'message': f'Your token is {token}'}, status.HTTP_200_OK)
    return Response({"message": "неверный код подтверждения."},
                    status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminCustomUser,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username', ]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = CustomUserSerializer(self.request.user)
        else:
            serializer = CustomUserPATCHSerializer(
                self.request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
