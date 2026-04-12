from django.conf import settings


def app_version(request):
    return {
        "APP_VERSION": getattr(settings, "APP_VERSION", ""),
        "RELEASE_NOTES": getattr(settings, "RELEASE_NOTES", []),
    }
