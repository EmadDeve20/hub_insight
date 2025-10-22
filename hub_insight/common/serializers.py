from rest_framework import serializers

class PaginationFilterSerializer(serializers.Serializer):
    p = serializers.IntegerField(
        required=False, help_text="A page number within the paginated result set."
    )
    page_size = serializers.IntegerField(
        required=False, help_text="Number of results to return per page."
    )
    all = serializers.BooleanField(required=False)



class SwaggerListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    page_size = serializers.IntegerField()
    results = serializers.ListField()

