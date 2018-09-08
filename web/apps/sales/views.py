import django_rq
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from guardian.shortcuts import get_objects_for_user
from apps.sales.forms.subscription import SubscriptionCreateForm
from apps.sales.models import PUSubscriptionStatus
from apps.services.hosting.tasks import create_hosting


class SubscriptionListView(TemplateView):

    template_name = 'sales/subscription-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_subscriptions'] = get_objects_for_user(
            self.request.user, 'sales.view_subscription')
        return context


class SubscriptionCreateView(CreateView):

    template_name = 'sales/subscription-create.html'
    form_class = SubscriptionCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer = self.request.user
        self.object.status = PUSubscriptionStatus.objects.get(slug='pending')
        self.object.period_months = 12
        self.object.save()
        django_rq.enqueue(create_hosting,
            subscription_id = self.object.id,
            service_id = form.cleaned_data.get('service').id,
            domain_name = form.cleaned_data.get('domain_name'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sales:subscription-list')
