from djangoldp.filters import LocalObjectFilterBackend
from djangoldp.views import LDPViewSet
from djangoldp.models import Model
from djangoldp_circle.models import Circle


class CirclesJoinableViewset(LDPViewSet):

    filter_backends = [LocalObjectFilterBackend]

    def get_queryset(self):
        return super().get_queryset().exclude(team__id=self.request.user.id)\
            .exclude(status="Private")\
            .exclude(status="Archived")
