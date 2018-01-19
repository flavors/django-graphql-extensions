from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404

from . import exceptions


def get_object_or_not_found(queryset, *args, **kwargs):
    try:
        return _get_object_or_404(queryset, *args, **kwargs)
    except (TypeError, ValueError, ValidationError, Http404):
        raise exceptions.NotFound(**kwargs)
