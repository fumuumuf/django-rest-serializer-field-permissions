"""
Drop in serializer mixins.
"""


class FieldPermissionSerializerMixin(object):
    """
    Mixin to your serializer class as follows:

        class PersonSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):

            family_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
            given_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
    """

    @property
    def fields(self):
        """
        Supercedes drf's serializers.ModelSerializer's fields property
        :return: a set of permission-scrubbed fields
        """
        ret = super(FieldPermissionSerializerMixin, self).fields
        request = self.context.get('request', None)

        fields_to_remove = []
        if request:
            for field_name, field in ret.items():
                if hasattr(field, 'check_permission') and (not field.check_permission(request)):
                    fields_to_remove.append(field_name)

        for field in fields_to_remove:
            ret.pop(field)

        return ret
