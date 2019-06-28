from django.contrib import admin
from .models import User
from .models import Post
from .models import Comment
from .models import Reaction
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)