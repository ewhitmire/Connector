from django.contrib import admin
from connector.models import *

admin.site.register(Member)
admin.site.register(Domain)
admin.site.register(Skill)
admin.site.register(Offer)
admin.site.register(Category)