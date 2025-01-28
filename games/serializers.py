from shared.serializers import BaseSerializer
from platforms.serializers import PlatformSerializer  
from categories.serializers import CategorySerializer 

class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'pegi': instance.get_pegi_display(),
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover':self.build_url(instance.cover.url),
            'price': float(instance.price), 
            'stock': instance.stock,
            'released_at': instance.released_at.isoformat(),
            'category': CategorySerializer(instance.category).serialize(),
            'platforms': PlatformSerializer(instance.platforms.all(), request=self.request).serialize(),
        }

class ReviewSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)
    
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'comment': instance.comment,
            'rating': instance.rating,
            'game': GameSerializer(instance.game).serialize(),
            #Esto no estoy seguro de si hay que hacer serializador de User!
            # 'author': UserSerializer(instance.author).serialize(),
            'created_at': instance.created_at.isoformat(),  
            'updated_at': instance.updated_at.isoformat(), 

        }
