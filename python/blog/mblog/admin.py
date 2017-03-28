from django.contrib import admin

from .models import Topic
from .models import Tag
from .models import Post
from .models import post_tag
from .models import PostDetails
from .models import User
from .models import Comment

# Register your models here.
admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(post_tag)
admin.site.register(PostDetails)
admin.site.register(User)
admin.site.register(Comment)
