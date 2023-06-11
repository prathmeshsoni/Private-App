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


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


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
            if userobj.is_staff == 2:
                # print('Fails');
                # messages.success(request, f'Failss.{userobj.is_staff}')
                # return redirect('/private/')

                try:
                    user = UserModel.objects.get(email=username)
                    user11 = authenticate( username = user , password = password)
                    if (user11) is None:
                        messages.success(request, 'Wrong Password.')
                        return redirect('/private/')

                    # login(request , user11)
                    request.session['private_admin'] = user
                    request.session['login_time'] = datetime.now().timestamp()
                    return redirect('/private/view/')

                except:
                    usee = None;

                user1 = authenticate( username = username , password = password)

                if (user1 or usee ) is None:
                    messages.success(request, 'Wrong Password.')
                    return redirect('/private/')

                # login(request , user1)
                request.session['private_admin'] = username
                request.session['login_time'] = datetime.now().timestamp()
                return redirect('/private/view/')


    # elif request.method == 'GET':
    return render(request , 'login.html',{"checkcon":0, "Title":"Private "})

    # elif 'username' in request.session:
    #     return redirect('/user/dashboard/')


def some_view(request):
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
    return check


def private_view(request,hid):
    check = some_view(request)
    if int(check) == 1:
        return redirect('/private/logout/')
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

            return redirect(f"/private/view/{hid}")
        else:
            if 'private_admin' in request.session:
                pro_list = Private_SubModel.objects.filter(private_id=hid)
                order = PrivateModel.objects.get(id=hid)
                d = PrivateForm()
                data = {'m':d,'private_master':'master','private_activee':'private_masterr','lists':pro_list,'order':order,"private_1":0, "checkcon":0}
            else:
                return redirect('/private/')
            return render(request , 'private.html', data)


def logout_private_admin(request):
    if 'private_admin' in request.session:
        del request.session['private_admin']
        del request.session['login_time']
    # logout(request)
    return redirect('/private/')


def admin_private_view(request):
    check = some_view(request)
    if int(check) == 1:
        return redirect('/private/logout/')
    else:
        if request.method == 'POST':
            try:
                id = request.POST.get('id')
                jj = PrivateModel.objects.get(id=id)
                d = PrivateForm(request.POST or None,instance=jj)
            except:
                try:
                    d = PrivateForm(request.POST or None)
                except Exception as e:
                    print("Error :: ", e)
            if d.is_valid():
                d.save()
                return redirect(f'/private/view/{id}')
        else:
            if 'private_admin' in request.session:
                d = PrivateForm()
                b = PrivateModel.objects.all()
                x = {'m':d,'list':b,'private_master':'master','private_active':'private_master', "private_1":0, "checkcon":0}
            else:
                return redirect('/private/')
        return render(request , 'private_des.html', x)


@api_view(['POST'])
def updatepra(request):
    id = request.POST.get('id')
    get_data = PrivateModel.objects.get(id = id)
    serializer = PrivateSerialize(get_data)
    return Response(serializer.data)

def remove_pri(request,hid):
    obj = PrivateModel.objects.get(id = hid)
    obj.delete()
    return redirect('/private/view/')

def remove_photo(request,hid):
    obj = Private_SubModel.objects.get(id = hid)
    jj = obj.private_id.id
    obj.delete()
    return redirect(f'/private/view/{jj}')


def download_data(request):
    if request.method == 'POST':
        condition_check = request.POST.get('check')
        print(condition_check)
        if int(condition_check) == 1:
            id = request.POST.get('id')
            try:
                folder_url = upload(id)
                a = {'url': folder_url, 'status': True}
            except:
                a = {'status': False}
        else:
            vall = request.POST.get('folder_id')
            folder_id = vall.split('/')[-1]
            try:
                folder_url = delete_drive(folder_id)
                a = {'url': folder_url, 'status': True}
            except:
                a = {'status': False}
        return JsonResponse(a)
    else:
        a = {'status': False}
        return JsonResponse(a)


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
        'parents': ['1B46tgqRWsSWw_EU-tGAWoUSUVqD71Psc']
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

    file_pathh = working_dir + '/private_info/uploads/text.txt'
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

        img_content = MediaFileUpload(working_dir + '/private_info/uploads/' +file_11, mimetype=img_type)
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


def delete_drive(folder_id):
    API_NAME = 'drive'
    API_VERSION = 'v3'
    service = Create_Service(API_NAME, API_VERSION)
    service.files().delete(fileId=folder_id).execute()

