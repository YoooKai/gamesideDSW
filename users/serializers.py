from shared.serializers import BaseSerializer


class TokenSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'user': UserSerializer(instance.user).serialize(),
            'key': str(instance.key),
            'created_at': instance.created_at.isoformat(),
        }


class UserSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'first_name': instance.name,
            'last_name': str(instance.key),
            'email': instance.email,
            'username': instance.username,
        }
