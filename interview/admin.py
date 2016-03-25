from django.contrib import admin
from .models import CandidateRating


class CandidateRatingAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'interviewer', 'rating',)
    search_fields = ('candidate__name',)


admin.site.register(CandidateRating, CandidateRatingAdmin)
