from django.contrib import admin

from .models import ShortenedURL, Visit, Analytic


class AnalyticInline(admin.StackedInline):
    model = Analytic


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'long_url', 'short_url')
    list_display_links = ('id',)
    list_filter = ('created_at', 'updated_at')

    def short_url(self, instance: ShortenedURL):
        return instance.short_url()

    short_url.short_description = 'Short URL'

    inlines = (AnalyticInline,)


@admin.register(Analytic)
class AnalyticAdmin(admin.ModelAdmin):
    pass


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'browser')
    list_display_links = ('id',)
    list_filter = ('platform', 'browser', 'session_key')
    readonly_fields = ('id', 'platform', 'browser', 'session_key')
