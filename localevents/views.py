from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            created_events = Event.objects.filter(organizer=profile)
            signedup_events = Event.objects.filter(eventsignup__user_registrant=profile)

            all_events = Event.objects.exclude(
                id__in=created_events
            ).exclude(
                id__in=signedup_events
            )

            context['created_events'] = created_events
            context['signedup_events'] = signedup_events
            context['all_events'] = all_events

        else:
            context['all_events'] = Event.objects.all()

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'
    context_object_name = 'event'
