CHOICES_LOOKUPS = ['exact', 'in']

TEXT_LOOKUPS = CHOICES_LOOKUPS + [
    'iexact', 'contains', 'icontains', 'startswith',
    'istartswith', 'endswith', 'iendswith', 'regex', 'iregex',
]

RANGE_LOOKUPS = ['exact', 'gt', 'gte', 'lt', 'lte']

DATETIME_LOOKUPS = RANGE_LOOKUPS + \
    ['date__' + lookup for lookup in RANGE_LOOKUPS] + \
    ['year', 'month', 'week_day', 'day', 'hour']
