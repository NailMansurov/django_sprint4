from django.contrib import admin
from .models import Post, Category, Comment, Location

admin.site.empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'text', 'category',
        'pub_date', 'location', 'is_published', 'created_at'
    )
    list_display_links = ('title', )
    list_editable = ('category', 'is_published', 'location')


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
