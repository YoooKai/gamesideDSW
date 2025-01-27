from shared.serializers import BaseSerializer


class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
            'logo': self.build_url(instance.logo.url),
            'cover': self.build_url(instance.cover.url()),
            'price': float(instance.price),
            'released_at': instance.released_at.isoformat(),
        }
