def get_user(instance):
    user = instance.request.user
    if user is None:
        token = Token.objects.get(key=instance.request.auth)
        user = token.user
    return user