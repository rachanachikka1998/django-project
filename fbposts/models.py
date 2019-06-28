from django.db import models
import django


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    pic_url = models.CharField(max_length=5000)


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    posted_by = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    post_content = models.CharField(max_length=10000, default=None)
    posted_at = models.DateTimeField(default=None)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_field = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    comment_field = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    comment_content = models.CharField(max_length=10000)
    commenter_id = models.ForeignKey('User', on_delete=models.CASCADE)
    commented_at=models.DateTimeField(null=True)



    def save(self, *args, **kwargs):
        if self.post_field == None:
            if self.comment_field != None:
                models.Model.save(self)
        elif self.comment_field == None:
            if self.post_field != None:
                models.Model.save(self)
        else:
            print("check post and comment conflicts")




class Reaction(models.Model):
    reactions=(('HAHA','HAHA'),('LIKE','LIKE'),('LOVE','LOVE'),('WOW','WOW'),('SAD','SAD'),('ANGRY','ANGRY'))
    reaction_type = models.CharField(max_length=5,choices=reactions)
    reactor = models.ForeignKey('User', on_delete=models.CASCADE)
    post_field = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    comment_field = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    types=(('post','post'),('comment','comment'))
    type=models.CharField(max_length=7,choices=types)

    def save(self,*args,**kwargs):
        if self.post_field==None:
            if self.comment_field!=None:
                models.Model.save(self)
        elif self.comment_field==None:
            if self.post_field!=None:
                models.Model.save(self)
        else:
            print("check post and comment conflicts")
    class Meta:
        unique_together=(("post_field","comment_field","reactor"),)



