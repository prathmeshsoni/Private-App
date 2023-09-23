from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.backends import UserModel
from Private.models import PrivateModel, Private_SubModel
from Private.forms import PrivateForm
from Private.serializer import PrivateSerialize
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.http import JsonResponse
from googleapiclient.http import MediaFileUpload
from Private.Google import Create_Service
import os


# 404 Page Not Found
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


# Private LogIn Screen
def admin_private(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        userobj = User.objects.filter(username = username).first()
        user_obj = User.objects.filter(email = username).first()
        if userobj:
            pass
        if user_obj:
            userobj = user_obj
        if (userobj) is None:
            messages.success(request, 'Username/Email not found.')
            return redirect(request.META.get('HTTP_REFERER'))

        if not (userobj).is_superuser:
            messages.success(request, "User Can't login")
            return redirect(request.META.get('HTTP_REFERER'))

        if (userobj).is_superuser:
            if userobj.is_staff:
                try:
                    user = UserModel.objects.get(email=username)
                    user11 = authenticate( username = user , password = password)
                    if (user11) is None:
                        messages.success(request, 'Wrong Password.')
                        return redirect('/')

                    # login(request , user11)
                    request.session['private_admin'] = user11.username
                    request.session['private_id'] = user11.id
                    request.session['login_time'] = datetime.now().timestamp()
                    return redirect('/view/')

                except:
                    usee = None;

                user1 = authenticate( username = username , password = password)

                if (user1 or usee ) is None:
                    messages.success(request, 'Wrong Password.')
                    return redirect('/')

                # login(request , user1)
                request.session['private_admin'] = user1.username
                request.session['private_id'] = user1.id
                request.session['login_time'] = datetime.now().timestamp()
                return redirect('/view/')


    # elif request.method == 'GET':
    return render(request , 'login.html',{"checkcon":0, "Title":"Private "})

    # elif 'username' in request.session:
    #     return redirect('/user/dashboard/')


# Private LogOut
def logout_private_admin(request):
    if 'private_admin' in request.session:
        del request.session['private_admin']
        del request.session['login_time']
        try:
            del request.session['private_id']
        except:
            pass
    # logout(request)
    return redirect('/')


# Logout Every 30 minutes
def some_view(request):
    return 0
    # Check if session has expired
    login_time = request.session.get('login_time')
    if login_time:
        login_time = datetime.fromtimestamp(login_time)
        if datetime.now() - login_time > timedelta(minutes=30):
            check = 1
        else:
            check = 0
    else:
        check = 1
    check = 0
    return check


# View All Details
def admin_private_view(request):
    check = some_view(request)
    if int(check) == 1:
        return redirect('/logout/')
    else:
        if request.method == 'POST':
            try:
                id = request.POST.get('id')
                jj = PrivateModel.objects.get(id=id)
                d = PrivateForm(request.POST or None,instance=jj,)
            except:
                d = PrivateForm(request.POST)
            if d.is_valid():
                user_id = request.session.get('private_id')
                user_obj = User.objects.get(id = user_id)
                private_data = d.save(commit=False)
                private_data.user = user_obj
                private_data.save()
                id = private_data.id
                return redirect(f'/view/{id}')
            else:
                return redirect(f'/view/')
        else:
            if 'private_admin' in request.session:
                d = PrivateForm()
                user2 = request.session.get('private_admin')
                user_obj2 = User.objects.get( username = user2)
                b = PrivateModel.objects.filter(user=user_obj2).order_by('-date_name')
                # b = PrivateModel.objects.all()
                x = {'m':d,'list':b,'private_master':'master','private_active':'private_master', "private_1":0, "checkcon":0}
            else:
                return redirect('/')
        return render(request , 'private_des.html', x)
        

# View All Photo, Add Photo 
def private_view(request,hid):
    check = some_view(request)
    if int(check) == 1:
        # call this fun logout_private_admin()
        return redirect('/logout/')
    else:
        if request.method == 'POST':
            id = request.POST.get("p_id")
            myfile = request.FILES.getlist("private_img")

            for f in myfile:
                chek = str(f).split('.')[-1]
                if (chek == "mp4"):
                    type = "video"
                else:
                    type = "photo"
                pro_obj = Private_SubModel()
                pri_id = PrivateModel.objects.get(id = id)
                pro_obj.private_id = pri_id
                pro_obj.private_img = f
                pro_obj.type = type
                pro_obj.save()

            return redirect(f"/view/{hid}")
        else:
            if 'private_admin' in request.session:
                user2 = request.session.get('private_admin')
                order = PrivateModel.objects.get(id=hid)
                if order.user.username == user2:
                    pro_list = Private_SubModel.objects.filter(private_id=hid)
                    d = PrivateForm()
                    data = {'m':d,'private_master':'master','private_activee':'private_masterr','lists':pro_list,'order':order,"private_1":0, "checkcon":0}
                else:
                    return redirect('/view/')
            else:
                return redirect('/')
            return render(request , 'private.html', data)


# Private Detail Function
@api_view(['POST'])
def updatepra(request):
    id = request.POST.get('id')
    get_data = PrivateModel.objects.get(id = id)
    serializer = PrivateSerialize(get_data)
    return Response(serializer.data)


# Delete Detail Fun
def remove_pri(request,hid):
    if 'private_admin' in request.session:
        user2 = request.session.get('private_admin')
        obj = PrivateModel.objects.get(id = hid)
        if obj.user.username == user2:
            obj.delete()
            return redirect('/view/')
        else:
            return redirect('/view/')
    else:
        return redirect('/')


# Delete Photo Fun
def remove_photo(request,hid):
    if 'private_admin' in request.session:
        user2 = request.session.get('private_admin')
        obj = Private_SubModel.objects.get(id = hid)
        if obj.private_id.user.username == user2:
            jj = obj.private_id.id
            obj.delete()
            return redirect(f'/view/{jj}')
        else:
            return redirect('/view/')
    else:
        return redirect('/')


# Upload Into Google Drive
def download_data(request):
    if request.method == 'POST':
        condition_check = request.POST.get('check')
        if int(condition_check) == 1:
            id = request.POST.get('id')
            try:
                folder_url = upload(id)
                a = {'url': folder_url, 'status': True}
            except Exception as e:
                print('ee1', e)
                a = {'status': False}
        else:
            vall = request.POST.get('folder_id')
            folder_id = vall.split('/')[-1]
            try:
                folder_url = delete_drive(folder_id)
                a = {'url': folder_url, 'status': True}
            except Exception as e:
                print('ee', e)
                a = {'status': False}
        return JsonResponse(a)
    else:
        a = {'status': False}
        return JsonResponse(a)


# Upload Folder, File, Photos/Videos Into Google Drive
def upload(id):
    order = PrivateModel.objects.get(id=id)
    folder_name = str(order.date_name)

    # Login Process Start# Download From console.cloud.google.com
    API_NAME = 'drive'
    API_VERSION = 'v3'
    service = Create_Service(API_NAME, API_VERSION)
    print('service :: ', service)
    # Login Process End

    request_body = {
        'role': 'reader',
        'type': 'anyone',
    }

    # Create a Folder
    folder_type = 'application/vnd.google-apps.folder'
    folder_metadata = {
        'name': folder_name,
        'mimeType': folder_type,
        'parents': ['1sVXo51JUcsULkQBRa2N-BqPEh-_LdzTj']
    }
    folder = service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()
    folder_id = folder.get('id')

    # Folder Permission
    permission_folder = service.permissions().create(
        fileId=folder_id,
        body=request_body
    ).execute()

    # Print Sharing URL FOLDER
    response_share_link_folder = service.files().get(
        fileId=folder_id,
        fields='webViewLink'
    ).execute()
    folder_url = response_share_link_folder['webViewLink']

    working_dir = os.getcwd()

    file_pathh = working_dir + '/uploads/text.txt'
    with open(file_pathh, "w") as file:
        file.write(str(order.private_description))

    text_file_type = 'text/plain'
    text_file_metadata = {
        'name': f'text.txt',
        'parents': [folder_id],
    }

    des_content = MediaFileUpload(file_pathh, mimetype=text_file_type)
    filess = service.files().create(
        body=text_file_metadata,
        media_body=des_content,
        fields='id'
    ).execute()
    file_ids = filess["id"]

    # File Permission
    permission_file = service.permissions().create(
        fileId=file_ids,
        body=request_body
    ).execute()

    # Upload a Images
    pro_list = Private_SubModel.objects.filter(private_id=id)
    for i in pro_list:
        file_11 = str(i.private_img)
        file_namee = str(file_11).split('/')[-1]
        chek = str(file_11).split('.')[-1]
        if (chek == "mp4"):
            img_type = 'video/mp4'
        else:
            if (chek == "png"):
                img_type = 'image/png'
            else:
                img_type = 'image/jpeg'
        img_metadata = {
            'name': f'{file_namee}',
            'parents': [folder_id],
        }

        img_content = MediaFileUpload(working_dir + '/uploads/' +file_11, mimetype=img_type)
        file = service.files().create(
            body=img_metadata,
            media_body=img_content,
            fields='id'
        ).execute()
        file_id = file["id"]

        # File Permission
        permission_file = service.permissions().create(
            fileId=file_id,
            body=request_body
        ).execute()
    return folder_url


# Delete Google Drive Folder
def delete_drive(folder_id):
    API_NAME = 'drive'
    API_VERSION = 'v3'
    service = Create_Service(API_NAME, API_VERSION)
    service.files().delete(fileId=folder_id).execute()
