from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
User = settings.AUTH_USER_MODEL


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FriendshipRequest(TrackableDateModel):
    from_user = models.ForeignKey(
        User, related_name="friendshiprequests_from", on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name="friendshiprequests_to", on_delete=models.CASCADE)
    message = models.CharField(max_length=200, blank=True)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    class Meta:
        verbose_name = _(u'friendship request')
        verbose_name_plural = _(u'friendship requests')
        unique_together = (('to_user', 'from_user'),)

    def __unicode__(self):
        return _(u'%(from_user)s wants to be friends with %(to_user)s') % {
            'from_user': unicode(self.from_user),
            'to_user': unicode(self.to_user),
        }

    def accept(self):
        Friendship.objects.befriend(self.from_user, self.to_user)
        self.delete()

    def decline(self):
        self.delete()

    def cancel(self):
        self.delete()


class FriendshipManager(models.Manager):
    def friends_of(self, user, shuffle=False):
        qs = User.objects.filter(friendship__friends__user=user)
        if shuffle:
            qs = qs.order_by('?')
        return qs

    def are_friends(self, user1, user2):
        friendship = Friendship.objects.get(user=user1)
        return bool(friendship.friends.filter(user=user2).exists())

    def befriend(self, user1, user2):
        # create for both users
        newFriend = Friendship(owner=user1, friend=user2)
        newFriend.save()
        newFriend2 = Friendship(friend=user1, owner=user2)
        newFriend2.save()

    def unfriend(self, user1, user2):
        Friendship.objects.filter(owner=user1, friend=user2).delete()
        Friendship.objects.filter(friend=user1, owner=user2).delete()
        FriendshipRequest.objects.filter(from_user=user1,
                                         to_user=user2).delete()
        FriendshipRequest.objects.filter(from_user=user2,
                                         to_user=user1).delete()


class Friendship(TrackableDateModel):
    owner = models.ForeignKey(
        User, related_name='friends', null=True, on_delete=models.CASCADE)
    friend = models.ForeignKey(
        User, related_name='Friendship', null=True, on_delete=models.CASCADE)
    objects = FriendshipManager()


class UserBlocks(TrackableDateModel):
    user = models.OneToOneField(
        User, related_name='user_blocks', on_delete=models.CASCADE)
    blocks = models.ManyToManyField(
        User, related_name='blocked_by_set')

    class Meta:
        verbose_name = verbose_name_plural = _(u'user blocks')

    def __unicode__(self):
        return _(u'Users blocked by %(user)s') % {'user': unicode(self.user)}

    def block_count(self):
        return self.blocks.count()
    block_count.short_description = _(u'Blocks count')

    def block_summary(self, count=7):
        block_list = self.blocks.all()[:count]
        return u'[%s%s]' % (u', '.join(unicode(user) for user in block_list),
                            u', ...' if self.block_count() > count else u'')
    block_summary.short_description = _(u'Summary of blocks')
