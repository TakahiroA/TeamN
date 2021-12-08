from django.urls import path
from . import views

app_name = 'taskapp'

urlpatterns = [
    path('',views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('month_with_schedule/<int:year>/<int:month>/',views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('registration/complete', views.RegistrationComp.as_view(), name='registration_complete'),
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('profile/<int:pk>/password', views.PasswordChange.as_view(), name='password'),
    path('profile/<int:pk>/password/complete', views.PasswordChangeComplete.as_view(), name='password_complete'),
]