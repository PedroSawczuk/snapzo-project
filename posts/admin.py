from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_published', 'created_at', 'view_count', 'like_count')
    list_filter = ('is_published', 'created_at', 'user')
    search_fields = ('user__username', 'content')
    prepopulated_fields = {'content': ('user',)}  
    ordering = ('-created_at',)
    readonly_fields = ('view_count', 'like_count', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'content', 'image', 'is_published')
        }),
        ('Contadores', {
            'fields': ('view_count', 'like_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),  
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)
