from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Disaster)
admin.site.register(Prediction)
admin.site.register(Location)
admin.site.register(AffectedArea)
admin.site.register(Profile)
admin.site.register(Updates)
admin.site.register(CommunityFeedback)
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Post)