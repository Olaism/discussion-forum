from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin

class CustomCreateModelMixin(CreateModelMixin):

    """
    Create a custom model instance.
    """
    def create(self, request, *args, **kwargs):
        user_token = User.objects.get(pk=kwargs.get('user_id')).key
        if request.auth != user_token:
            return Response({"error": "You can't peform a post request"}, status=status.HTTP_401_UNAUTHORIZED, headers=headers)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(self.request.user)