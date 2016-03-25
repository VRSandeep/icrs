from django import forms
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import serializers, generics, status

from .models import CandidateRating


# Serializers define the API representation.
class RatingSerializer(serializers.ModelSerializer):

    candidate = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=False))
    interviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=True), required=False)

    class Meta:
        model = CandidateRating
        fields = ('candidate', 'interviewer', 'rating')

    def __init__(self, *args, **kwargs):
        super(RatingSerializer, self).__init__(*args, **kwargs)
        kargs = kwargs.get('data', None)
        if not kargs:
            return


class RatingCreateUpdate(generics.GenericAPIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = (IsAdminUser,)
    queryset = CandidateRating.objects.all()
    serializer_class = RatingSerializer
    allowed_methods = ('POST',)

    def post(self, request, *args, **kwargs):
        # request.data['interviewer'] = request.user
        request_data_cpy = request.data.copy()
        request_data_cpy['interviewer'] = request.user.id
        serializer = RatingSerializer(data=request_data_cpy)
        if serializer.is_valid():
            try:
                # Allow Update only before all interviewers voted?
                cr = CandidateRating.objects.get(interviewer=request.user, candidate__id=request.data['candidate'])
                cr.rating = request.data['rating']
                cr.save()
                return Response(status=status.HTTP_200_OK)
            except CandidateRating.DoesNotExist:
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_previous_candidates(request):
    """
    Loads Candidate Ratings
    """
    from django.db.models import Avg

    staff_size = User.objects.filter(is_staff=True).count()
    candidates = User.objects.filter(is_staff=False).order_by('date_joined')[:50]

    candidate_ratings=[]
    for candidate in candidates:
        rating = CandidateRating.objects.filter(candidate=candidate)

        s = { 'candidate': candidate }

        # All interviewers have rated candidate
        if rating.count() == staff_size:

            s['rating'] = rating.aggregate(Avg('rating')).values()[0]
            s['my_rating'] = rating.filter(interviewer=request.user)[0]
        else:

            # Don't load avg if all interviewers haven't finished rating candidate
            s['rating'] = 'NA'
            r = rating.filter(interviewer=request.user)
            if r:
                s['my_rating'] = r[0]
            else:
                s['my_rating'] = 'NA'
        candidate_ratings.append(s)
    return candidate_ratings
