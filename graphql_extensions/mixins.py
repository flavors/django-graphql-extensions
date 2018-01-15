from . import exceptions


class RetrieveMixin(object):

    @classmethod
    def get_queryset(cls, context):
        assert cls.queryset is not None, (
            '`{}` should either include a `queryset` attribute, '
            'or override the `get_queryset()` method.'.format(cls.__name__)
        )

        return cls.queryset.all()

    @classmethod
    def get_object(cls, context, **kwargs):
        queryset = cls.get_queryset(context)
        try:
            return queryset.get(**kwargs)
        except queryset.model.DoesNotExist:
            raise exceptions.NotFound(**kwargs)


class UpdateMixin(RetrieveMixin):

    @classmethod
    def validate(cls, context, instance, **args):
        return args

    @classmethod
    def update(cls, context, id, **args):
        instance = cls.get_object(context, id=id)
        validated_data = cls.validate(context, instance, **args)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        cls.perform_update(instance)
        return instance

    @classmethod
    def perform_update(cls, instance):
        instance.save()
