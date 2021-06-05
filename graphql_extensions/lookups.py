CHOICES_LOOKUPS = ['exact', 'in']

TEXT_LOOKUPS = CHOICES_LOOKUPS + [
    'iexact', 'contains', 'icontains', 'startswith',
    'istartswith', 'endswith', 'iendswith', 'regex', 'iregex',
]

RANGE_LOOKUPS = ['exact', 'gt', 'gte', 'lt', 'lte']

DATE_UNITS = ['year', 'month', 'week_day', 'day']

DATE_LOOKUPS = RANGE_LOOKUPS + DATE_UNITS

DATETIME_LOOKUPS = RANGE_LOOKUPS + DATE_UNITS + ['hour'] + \
    ['date__' + lookup for lookup in RANGE_LOOKUPS]
