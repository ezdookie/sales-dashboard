from django.urls import path
from apps.services.hosting.views import (HostingListView, HostingDetailsView,
    HostingCreateUserView, HostingDeleteUserView)

app_name = "services"

urlpatterns = [
    path('<str:category>/', HostingListView.as_view(), name='list'),

    # Hosting
    path('hosting/<int:service_id>/details/', HostingDetailsView.as_view(), name='hosting-details'),
    path('hosting/<int:service_id>/create-user/', HostingCreateUserView.as_view(), name='hosting-create-user'),
    path('hosting/<int:service_id>/users/<int:user_id>/delete', HostingDeleteUserView.as_view(), name='hosting-delete-user'),
]
