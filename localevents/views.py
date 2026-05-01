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

            created = Event.objects.filter(organizer=profile)
            signed = Event.objects.filter(eventsignup__user_registrant=profile)

            other = Event.objects.exclude(organizer=profile)
            other = other.exclude(eventsignup__user_registrant=profile)

            context['created_events'] = created
            context['signed_events'] = signed
            context['all_events'] = other

        else:
            context['all_events'] = Event.objects.all()

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'
    context_object_name = 'event'
