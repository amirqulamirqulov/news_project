from django.contrib import admin
from .models import Category, News, Contact, Comment


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['title']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish_time', 'status']
    list_filter = ['status', 'created_time', 'publish_time', 'category']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_time']


admin.site.register(Contact)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['created_time', 'active']
    search_fields = ['body', 'user']
    actions = ['disable_comments', 'active_comments']

    def diable_comments(self, request, queryset):
        queryset.update(active=False)


    def active_comments(self, request, queryset):
        queryset.update(active=True)
