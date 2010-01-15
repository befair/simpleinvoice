from django.conf import settings

def common_processor(request):
	return {
		'MEDIA_URL'	: settings.MEDIA_URL,
	}

