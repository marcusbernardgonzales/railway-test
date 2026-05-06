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
        hasattr(user, "profile") and
        user.groups.filter(name="Commission Maker").exists()
        or user.is_superuser
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and hasattr(self.request.user, "profile"):
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

        return context


class ApplyToJobView(LoginRequiredMixin, View):
    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        if hasattr(request.user, "profile"):
            CommissionService.apply_to_job(job, request.user.profile)

        return redirect(job.commission.get_absolute_url())


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

        if self.request.POST:
            context['formset'] = JobFormSet(self.request.POST)
        else:
            context['formset'] = JobFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        form.instance.maker = self.request.user.profile

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

        return redirect(self.object.get_absolute_url())


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_commission_maker(request.user):
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = JobFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = JobFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.save()

            CommissionService.update_commission_status(self.object)

        return redirect(self.object.get_absolute_url())
