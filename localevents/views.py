from django.views import View
from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect, render

from .models import Event, EventSignup
from .forms import GuestSignupForm, EventForm


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            created = Event.objects.filter(organizer=profile)
            signed = Event.objects.filter(signups__user_registrant=profile)

            other = Event.objects.exclude(organizer=profile)
            other = other.exclude(signups__user_registrant=profile)

            context['created_events'] = created
            context['signed_events'] = signed
            context['all_events'] = other

        else:
            context['all_events'] = Event.objects.all()

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'

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

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if request.user.is_authenticated:
            return redirect(event.get_absolute_url())

        form = GuestSignupForm()
        return render(request, 'localevents/event_signup.html', {
            'form': form,
            'event': event
        })

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if event.signups.count() >= event.event_capacity:
            return redirect(event.get_absolute_url())

        if request.user.is_authenticated:
            profile = request.user.profile

            if not event.organizer.filter(id=profile.id).exists():
                EventSignup.objects.get_or_create(
                    event=event,
                    user_registrant=profile,
                )

            return redirect(event.get_absolute_url())

        form = GuestSignupForm(request.POST)

        if form.is_valid():
            signup = form.save(commit=False)
            signup.event = event
            signup.save()

        return redirect(event.get_absolute_url())
    
    
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        profile = request.user.profile

        if profile.role != 'Event Organizer':
            return redirect('localevents:event_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.organizer.add(self.request.user.profile)
        return response