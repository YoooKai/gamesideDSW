from games.serializers import GameSerializer
from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


class OrderSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'key': instance.get_key(),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'user': UserSerializer(instance.user).serialize(),
            'games': GameSerializer(instance.games.all(), request=self.request).serialize(),
            'price': instance.price,
        }
