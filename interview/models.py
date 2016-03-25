from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class CandidateRating(models.Model):

    candidate = models.ForeignKey(User, null=False, related_name='candidate')
    interviewer = models.ForeignKey(User, null=False, related_name='interviewer')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = 'Candidate Rating'
        verbose_name_plural = 'Candidate Ratings'
        unique_together = (('candidate', 'interviewer'),)

    def __unicode__(self):
        return u'%s' % self.rating

    def clean(self):
        if self.candidate.is_staff:
            raise ValidationError({'candidate': ValidationError('Candidate cannot be an interviewer')})
        if not self.interviewer.is_staff:
            raise ValidationError({'interviewer': ValidationError('Interviewer has to be a staff member')})
        super(CandidateRating, self).clean()

    def save(self, **kwargs):
        self.clean()
        return super(CandidateRating, self).save(**kwargs)
