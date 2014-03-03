from django.db import models

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from cubi.functions import minute_to_string

class WaitConvert(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s (%s)' % (self.user.nickname, self.user.email, minute_to_string(self.created))

    def convert(self):
        self.user.type = '2'
        self.user.save()