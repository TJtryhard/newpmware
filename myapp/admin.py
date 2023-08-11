from django.contrib import admin
from .models import Users, Projects, Announcement, KickOff, Milestones, Closure

# Register your models here.
admin.site.register(Projects)
admin.site.register(Users)
admin.site.register(Announcement)
admin.site.register(KickOff)
admin.site.register(Milestones)
admin.site.register(Closure)


