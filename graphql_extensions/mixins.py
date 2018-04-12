from graphene.types.mutation import MutationOptions

from .shortcuts import get_object_or_not_found


class RetrieveOptions(MutationOptions):
    lookup_field = 'pk'
    lookup_argument = 'id'


class RetrieveMixin:

    @classmethod
    def __init_subclass_with_meta__(cls, _meta=None, lookup_field=None,
                                    lookup_argument=None, **options):
        if _meta is None:
            _meta = RetrieveOptions(cls)

        if lookup_field is not None:
            _meta.lookup_field = lookup_field

        if lookup_argument is not None:
            _meta.lookup_argument = lookup_argument

        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def get_queryset(cls, context):
        assert cls.queryset is not None, (
            '`{}` should either include a `queryset` attribute, '
            'or override the `get_queryset()` method.'.format(cls.__name__)
        )

        return cls.queryset.all()

    @classmethod
    def get_object(cls, context, **kwargs):
        assert cls._meta.lookup_argument in kwargs, (
            'Expected mutation {0} to be called with argument '
            'named "{1}". Fix your argument list, or set the '
            '`.lookup_field` on the {0}.Meta class.'
            .format(cls.__name__, cls._meta.lookup_argument)
        )

        filter_kwargs = {
            cls._meta.lookup_field: kwargs[cls._meta.lookup_argument],
        }

        queryset = cls.get_queryset(context)
        return get_object_or_not_found(queryset, **filter_kwargs)


class UpdateMixin(RetrieveMixin):

    @classmethod
    def validate(cls, context, instance, **data):
        return data

    @classmethod
    def update(cls, context, **kwargs):
        instance = cls.get_object(context, **kwargs)
        validated_data = cls.validate(context, instance, **kwargs)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        cls.perform_update(instance)
        return instance

    @classmethod
    def perform_update(cls, instance):
        instance.save()
