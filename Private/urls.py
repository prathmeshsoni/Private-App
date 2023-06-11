from django.urls import path
from . import views


urlpatterns = [
    path('',views.admin_private),
    path('view/',views.admin_private_view),
    path('view/<int:hid>',views.private_view),
    path('logout/',views.logout_private_admin),
    path('updatepra/',views.updatepra),
    path('remove_pri/<int:hid>',views.remove_pri),
    path('remove_photo/<int:hid>',views.remove_photo),
    path('download_data/', views.download_data),
]
