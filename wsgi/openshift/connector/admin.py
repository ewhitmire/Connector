from django.contrib import admin
from connector.models import *
import autocomplete_light

admin.site.register(Member)
admin.site.register(Domain)
admin.site.register(Skill)
admin.site.register(Offer)
admin.site.register(Category)

class TagAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(Tag)
admin.site.register(Tag)