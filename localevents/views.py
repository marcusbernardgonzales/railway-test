from django.views import View
from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
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


class BaseSignupView(View):

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if not self.check_capacity(event):
            return redirect(self.get_redirect_url(event))

        if request.user.is_authenticated:
            if not self.check_ownership(event, request.user):
                return redirect(self.get_redirect_url(event))

        self.create_signup(event, request)

        return redirect(self.get_redirect_url(event))

    def check_capacity(self, event):
        raise NotImplementedError

    def check_ownership(self, event, user):
        raise NotImplementedError

    def create_signup(self, event, request):
        raise NotImplementedError

    def get_redirect_url(self, event):
        raise NotImplementedError


class EventSignupView(BaseSignupView):

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if request.user.is_authenticated:
            return redirect(event.get_absolute_url())

        form = GuestSignupForm()
        return render(request, 'localevents/event_signup.html', {
            'form': form,
            'event': event
        })

    def check_capacity(self, event):
        return event.signups.count() < event.event_capacity

    def check_ownership(self, event, user):
        profile = user.profile
        return not event.organizer.filter(id=profile.id).exists()

    def create_signup(self, event, request):
        if request.user.is_authenticated:
            EventSignup.objects.get_or_create(
                event=event,
                user_registrant=request.user.profile,
            )
        else:
            form = GuestSignupForm(request.POST)

            if form.is_valid():
                signup = form.save(commit=False)
                signup.event = event
                signup.save()

    def get_redirect_url(self, event):
        return event.get_absolute_url()
    
    
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_create.html'

    def form_valid(self, form):
        if not self.request.user.groups.filter(name="Event Organizer").exists():
            return redirect('localevents:event_list')

        response = super().form_valid(form)
        self.object.organizer.add(self.request.user.profile)
        return response


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_update.html'
    context_object_name = 'event'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.groups.filter(name="Event Organizer").exists():
            return redirect('localevents:event_list')

        event = self.get_object()

        if not event.organizer.filter(id=request.user.profile.id).exists():
            return redirect('localevents:event_detail', pk=event.pk)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        event = self.get_object()

        if not self.request.user.groups.filter(name="Event Organizer").exists():
            return redirect('localevents:event_list')

        if not event.organizer.filter(id=self.request.user.profile.id).exists():
            return redirect('localevents:event_detail', pk=event.pk)

        response = super().form_valid(form)

        if self.object.signups.count() >= self.object.event_capacity:
            self.object.status = "Full"
        else:
            self.object.status = "Available"

        self.object.save()

        return response
