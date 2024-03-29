from django.urls import path
from django.contrib.auth import views as auth_views
from passwords import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logged_out.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='auth/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),
    path('list/', views.PasswordListView.as_view(), name='password_list'),
    path('create/', views.PasswordCreateView.as_view(), name='password_create'),
    path('delete/<int:pk>/', views.PasswordDeleteView.as_view(), name='password_delete'),
    path('generator/', views.generator, name='generator'),
]