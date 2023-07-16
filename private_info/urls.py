"""private_info URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from Private.models import PrivateModel, Private_SubModel
from django.shortcuts import redirect
from Private.views import some_view
from django.contrib import messages
from django.contrib.auth.models import User


# from django.conf.urls import url as url_e


# def custom_login_required(view_func):
#     def wrapper(request, *args, **kwargs):
#         check = some_view(request)
#         if int(check) == 1:
#             return redirect('/logout/')
#         else:
#             if request.session.get('private_admin'):
#                 # user2 = request.session.get('private_admin')
#                 # user_obj2 = User.objects.get( username = user2)
#                 # 
#                 s = view_func(request, *args, **kwargs)
#                 messages.success(request,   check)
#                 return redirect('/view/61')
#                 # print(view_func(request, *args, **kwargs))
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return redirect('/')
        
#     return wrapper


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        check = some_view(request)
        if int(check) == 1:
            return redirect('/logout/')
        else:
            if request.session.get('private_admin'):
                user2 = request.session.get('private_admin')
                link = request.path.split('uploads/')[1]
                check = Private_SubModel.objects.get(private_img=link)
                # messages.success(request,   f'{check.private_id.user.username} {user2}')
                if str(check.private_id.user.username).lower() == str(user2).lower():
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('/view/')
            else:
                return redirect('/')
        
    return wrapper


@custom_login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


urlpatterns = [
    path('admin_side/', admin.site.urls),
    path('',include('Private.urls')),
    path('user/',include('User.urls')),
    re_path(r'^hit/uploads/(?P<path>.*)$', protected_serve,{'document_root':settings.MEDIA_ROOT}),
]

handler404 = "Private.views.page_not_found_view"