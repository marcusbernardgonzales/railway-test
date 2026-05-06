from .models import Commission, Job, JobApplication


class CommissionService:
    @staticmethod
    def apply_to_job(job, profile):
        if job.status == 'Full':
            return

        if job.applications.filter(applicant=profile).exists():
            return

        application = JobApplication.objects.create(
            job=job,
            applicant=profile
        )

        CommissionService.update_job_status(job)
        CommissionService.update_commission_status(job.commission)

        return application

    @staticmethod
    def update_job_status(job):
        accepted = job.applications.filter(status='Accepted').count()

        if accepted >= job.manpower_required:
            job.status = 'Full'
            job.save()

    @staticmethod
    def update_commission_status(commission):
        jobs = commission.jobs.all()

        if jobs.exists() and all(j.status == 'Full' for j in jobs):
            commission.status = 'Full'
            commission.save()
