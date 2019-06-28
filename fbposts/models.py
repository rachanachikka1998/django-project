from django.db import models
import django


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, default="")
    pic_url = models.CharField(max_length=5000, default="")


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    posted_by = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    post_content = models.CharField(max_length=10000, default=None)
    posted_at = models.DateTimeField(default=None)
    reactions = models.ForeignKey('Reaction', on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    id1 = models.ForeignKey('Post',  on_delete=models.CASCADE,null=True)
    id2 = models.ForeignKey('self',  on_delete=models.CASCADE,null=True)
    type = models.BooleanField()
    comment_content = models.CharField(max_length=10000, default="")
    reactions = models.ForeignKey('Reaction', on_delete=models.CASCADE, null=True)
    commenter_id = models.ForeignKey('User', on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = (("id1", "id2"),)



class Reaction(models.Model):
    reactions=(('HAHA','HAHA'),('LIKE','LIKE'),('LOVE','LOVE'),('WOW','WOW'),('SAD','SAD'),('ANGRY','ANGRY'))
    reaction_type=models.CharField(max_length=5,choices=reactions,default=None)
    reactor_id=models.ForeignKey('User',on_delete=models.CASCADE,default=None)
    reacted_to_post=models.ForeignKey('Post',on_delete=models.CASCADE,null=True)
    reacted_to_comment=models.ForeignKey('Comment',on_delete=models.CASCADE,null=True)
    type = models.BooleanField(default=True)

    class Meta:
        unique_together=(("reacted_to_post","reacted_to_comment"),)


