from shared.serializers import BaseSerializer
from games.serializers import GameSerializer  

class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'key': str(instance.key),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            #'user': ???
            'games': GameSerializer(instance.games.all(), request=self.request).serialize(), 
        }