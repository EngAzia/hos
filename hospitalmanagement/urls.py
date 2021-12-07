
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LogoutView

#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),

    path('',include("hospital.url")),
    path('/logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),
    path(r'^jet/', include(('jet.urls', 'jet'))),
    path(r'^jet/dashboard/', include('jet.dashboard.urls', namespace='jet-dashboard')),



]





