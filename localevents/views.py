from django.views import View
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect

from .models import Event, EventSignup
from .forms import GuestSignupForm


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
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object

        signup_count = event.signups.count()
        is_full = signup_count >= event.event_capacity

        is_owner = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            is_owner = event.organizer.filter(id=profile.id).exists()

        context['signup_count'] = signup_count
        context['is_full'] = is_full
        context['is_owner'] = is_owner
        context['can_signup'] = not is_full and not is_owner

        return context

class EventSignupView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if event.signups.count() >= event.event_capacity:
            return redirect(event.get_absolute_url())
        
        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            if not event.organizer.filter(id=profile.id).exists():
                EventSignup.objects.create(
                    event=event,
                    user_registrant=profile,
                )
            
            return redirect(event.get_absolute_url())

        return redirect('localevents:guest_signup_form', pk=event.pk)
    
class GuestSignupFormView(FormView):
    template_name = 'localevents/signup_form.html'
    form_class = GuestSignupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        context['event'] = event
        return context
    
    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])

        signup = form.save(commit=False)
        signup.event = event
        signup.save()

        return redirect(event.get_absolute_url())