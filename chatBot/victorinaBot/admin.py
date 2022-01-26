from django.contrib import admin
from .models import Question, Statistic, Channel, ChannelQuestion, Config


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change) -> None:
        super().save_model(request, obj, form, change)

admin.site.register(Question)
admin.site.register(Statistic)
admin.site.register(ChannelQuestion)
# admin.site.register(Channel)
admin.site.register(Config)
