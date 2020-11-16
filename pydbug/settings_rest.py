from datetime import timedelta
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    )
}

REST_USE_JWT = True
CORS_ORIGIN_ALLOW_ALL = True
JWT_AUTH = {
    # 'JWT_PAYLOAD_HANDLER': 'piirs.utils.jwt_payload_handler'
}

OLD_PASSWORD_FIELD_ENABLED = True
