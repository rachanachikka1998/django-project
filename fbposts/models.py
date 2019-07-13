from django.db import models

# Create your models here.
from fbposts.constants import Reactions


class User(models.Model):
    username = models.CharField(max_length=100)
    pic_url = models.URLField()


class Post(models.Model):
    posted_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="posts")
    post_content = models.TextField(null=False,blank=False)
    posted_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    comment_content = models.TextField()
    commenter = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comments")
    commented_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        are_both_comment_and_post_none = self.comment is None and self.post is None
        are_both_comment_and_post_not_none = self.comment is not None and self.post is not None
        if are_both_comment_and_post_none or are_both_comment_and_post_not_none:
            raise Exception("give appropriate post and comment ids")
        super(Comment, self).save()


class Reaction(models.Model):
    reactions = (
        (Reactions.HAHA.value, Reactions.HAHA.value), (Reactions.LIKE.value, Reactions.LIKE.value),
        (Reactions.LOVE.value, Reactions.LOVE.value), (Reactions.WOW.value, Reactions.WOW.value),
        (Reactions.SAD.value, Reactions.SAD.value), (Reactions.ANGRY.value, Reactions.ANGRY.value))

    reaction_type = models.CharField(max_length=5, choices=reactions)
    reactor = models.ForeignKey('User', on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name="reactions")
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, related_name="reactions")

    def save(self, *args, **kwargs):
        are_both_comment_and_post_none = self.comment is None and self.post is None
        are_both_comment_and_post_not_none = self.comment is not None and self.post is not None
        if are_both_comment_and_post_none or are_both_comment_and_post_not_none:
            raise Exception("give appropriate post and comment ids")
        super(Reaction, self).save()

    class Meta:
        unique_together = (("post", "reactor"), ("comment", "reactor"),)
