SECRET_KEY = "django-insecure-9@o-=ra!l(rd^$1vrxky*eb+@jx__gs287xaoxwo=9!trbp%c#fsfds"
DEBUG = True
ALLOWED_HOSTS = []
#
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "uzum_base_payment",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "5432",
    },
}
CORS_ALLOWED_ORIGINS = ()
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "access-control-allow-methods",
    "access-control-allow-origin",
)
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
