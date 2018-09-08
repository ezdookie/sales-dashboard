import django_rq
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from guardian.shortcuts import get_objects_for_user
from apps.services.hosting.forms import CreateHostingUser
from apps.services.hosting.tasks import create_hosting_user, delete_hosting_user
from apps.services.models import PUCustomerService, PUCustomerServiceHostingUser


class HostingListView(TemplateView):

    template_name = 'services/hosting/hosting-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_services'] = get_objects_for_user(
            self.request.user, 'services.view_cservice')
        return context


class HostingDetailsView(TemplateView):

    template_name = 'services/hosting/hosting-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_cservice'] = PUCustomerService.objects.get(pk=self.kwargs.get('service_id'))
        has_perms = self.request.user.has_perm('services.view_cservice', context['obj_cservice'])
        return context if has_perms else None


class HostingCreateUserView(CreateView):

    template_name = 'services/hosting/user-create.html'
    form_class = CreateHostingUser

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.cservice = self.customerService
        self.object.save()
        task_data = form.cleaned_data
        task_data.update({'cservice_id': self.customerService.id})
        django_rq.enqueue(create_hosting_user, **task_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('services:hosting-details', args=[self.customerService.id])

    def dispatch(self, request, *args, **kwargs):
        self.customerService = PUCustomerService.objects.get(pk=self.kwargs.get('service_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_cservice'] = self.customerService
        return context


class HostingDeleteUserView(DeleteView):

    template_name = 'services/hosting/user-delete.html'
    model = PUCustomerServiceHostingUser
    pk_url_kwarg = 'user_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_data = {
            'cservice_id': self.customerService.id,
            'username': self.object.username
        }
        django_rq.enqueue(delete_hosting_user, **task_data)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('services:hosting-details', args=[self.customerService.id])

    def post(self, request, *args, **kwargs):
        self.customerService = PUCustomerService.objects.get(pk=self.kwargs.get('service_id'))
        return super().post(request, *args, **kwargs)
