from django_elasticsearch_dsl import DocType, Index, fields
from shirts.models import Shirt, Comment


shirts = Index('shirts')

@shirts.doc_type
class ShirtDocument(DocType):

    comments = fields.NestedField(properties={
        'text': fields.TextField(),
    })

    class Meta:
        model = Shirt

        fields = [
            'title',
            'description',
        ]
        related_models = [Comment]

    def get_instances_from_related(self, related_instance):
        return related_instance.shirt
