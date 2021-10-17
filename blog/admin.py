from django.contrib import admin

from blog.models import Post, PostFile, Like, Comment, Report


class PostFileInlineAdmin(admin.TabularInline):
    model = PostFile


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'publish_date')
    list_display_links = ('id', 'author')
    inlines = [PostFileInlineAdmin]


class PostFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'file', 'post')
    list_display_links = ('id', 'type')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user')
    list_display_links = ('id', 'post')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'post', 'author')
    list_display_links = ('id', 'text')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'text', 'post', 'author')
    list_display_links = ('id', 'type', 'text')


admin.site.register(Post, PostAdmin)
admin.site.register(PostFile, PostFileAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Report, ReportAdmin)
