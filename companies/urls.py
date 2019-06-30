from django.urls import path

from .views import companies, company_new, company_edit, company_detail

app_name = 'companies'
urlpatterns = [
    path('', companies, name='index'),
    # path('new', views.new, name='new')
    path("new", company_new, name="new"),
    path("<int:pk>/edit", company_edit, name="edit"),
    path("<int:pk>/view", company_detail, name="view")
]