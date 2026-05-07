from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, Value, IntegerField

from .models import Commission, Job
from .forms import CommissionForm, JobFormSet
from .services import CommissionService


def is_commission_maker(user):
    return (
        user.is_authenticated and
        hasattr(user, 'profile') and
        (
        user.groups.filter(name='Commission Maker').exists()
        or user.is_superuser
        )
    )


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'
    context_object_name = 'commissions'

    def get_queryset(self):
        return Commission.objects.annotate(
            status_order=Case(
                When(status='Open', then=Value(0)),
                When(status='Full', then=Value(1)),
                When(status='Completed', then=Value(2)),
                When(status='Discontinued', then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by('status_order', '-created_on')


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'
    context_object_name = 'commission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.object

        jobs = commission.jobs.all()

        total_required = sum(j.manpower_required for j in jobs)
        accepted = sum(
            j.applications.filter(status='Accepted').count()
            for j in jobs
        )

        context['jobs'] = jobs
        context['total_manpower'] = total_required
        context['open_manpower'] = total_required - accepted

        context['is_owner'] = (
            self.request.user.is_authenticated and
            hasattr(self.request.user, 'profile') and
            commission.maker == self.request.user.profile
        )

        return context


    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
                profile = self.request.user.profile

                created = Commission.objects.filter(maker=profile)
                applied = Commission.objects.filter(
                    jobs__applications__applicant=profile
                ).distinct()

                context['created'] = created
                context['applied'] = applied

                context['commissions'] = context['commissions'].exclude(
                    id__in=created.union(applied)
                )

            return context


class BaseJobActionView(View):
    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        if not self.check_capacity(job):
            return redirect(self.get_redirect_url(job))

        if request.user.is_authenticated:
            if not self.check_permission(job, request.user):
                return redirect(self.get_redirect_url(job))

        self.perform_action(job, request)

        return redirect(self.get_redirect_url(job))

    def check_capacity(self, job):
        raise NotImplementedError

    def check_permission(self, job, user):
        raise NotImplementedError

    def perform_action(self, job, request):
        raise NotImplementedError

    def get_redirect_url(self, job):
        return job.commission.get_absolute_url()

class ApplyToJobView(BaseJobActionView):
    def check_capacity(self, job):
        accepted = job.applications.filter(status='Accepted').count()
        return accepted < job.manpower_required

    def check_permission(self, job, user):
        if not hasattr(user, 'profile'):
            return False

        # prevent duplicate applications
        return not job.applications.filter(applicant=user.profile).exists()

    def perform_action(self, job, request):
        if hasattr(request.user, 'profile'):
            CommissionService.apply_to_job(job, request.user.profile)


class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_commission_maker(request.user):
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = JobFormSet(self.request.POST or None)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if not hasattr(self.request.user, 'profile'):
            return redirect('/')

        form.instance.maker = self.request.user.profile

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())

        return self.form_invalid(form)


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_commission_maker(request.user):
            return redirect('/')
        
        obj = self.get_object()

        if not hasattr(request.user, 'profile'):
            return redirect('/')
        
        if obj.maker != request.user.profile:
            return redirect(obj.get_absolute_url())
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = JobFormSet(self.request.POST or None, instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.save()

            CommissionService.update_commission_status(self.object)

            return redirect(self.object.get_absolute_url())

        return self.form_invalid(form)
