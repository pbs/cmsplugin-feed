from django.db import models
from django.utils.translation import ugettext as _
from cms.models import CMSPlugin

class Feed(CMSPlugin):
    name = models.CharField(verbose_name=_('name'),max_length=255,
                            null=True, blank=True)
    feed_url = models.URLField(verbose_name=_('feed URL'),verify_exists=True)

    def __unicode__(self):
        return self.name
