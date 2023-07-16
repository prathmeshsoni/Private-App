from .models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

#Change User Password
def change_password(request):
    if 'userid' in request.session:
        if request.method == 'POST':
            current = request.POST.get('old_password')
            new_pas = request.POST.get('new_password1')

            user2 = request.session.get('userid')
            user = User.objects.get(id=user2)
            un = user.username
            check = user.check_password(current)
            if check==True:
                user.set_password(new_pas)
                user.save()
                a = {'status': True}
                return JsonResponse(a)
            else:
                a = {'status': False}
                return JsonResponse(a)
        else:
            try:
                user2 = request.session.get('userid')
                count = cart_count(user2)
                user_obj2 = User.objects.get(id=user2)
                alldata = add_to_cart.objects.filter(user=user_obj2)
                total_price = cartdetail(alldata,user2)
            except:
                count = 0
                alldata = 0
                total_price = 0
            return render(request,"user/change-password.html",{'change_active':'password_master','cartt':alldata,'total_price':total_price,'cart_val':count})
    else:
        messages.success(request, 'First You Need to Login')
        return redirect('/user/accounts/login/')


#Registration Page for User
def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
                a = {'status': True,'exists':'existuser'}
                return JsonResponse(a)

            if User.objects.filter(email = email).first():
                a = {'status': True,'exists':'existemail'}
                return JsonResponse(a)

            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email, username, auth_token)
            a = {'status': True,'create':'usercreate','u_name':username}
            return JsonResponse(a)


        except:
            print("e");

            a = {'status': False}
        # return JsonResponse(a)


    else:
        if 'userid' in request.session:
            return redirect('/')
        else:
            return render(
                request , 
                'user/register.html',
                {'cartc':'2'}
            )


#Account Activation Mail Send
def send_mail_after_registration(email,username , token):
    email_template_name = 'user/verifymail.html'
    parameters = {
        'domain' : 'private-app.monarksoni.com/user/verify',
        'token' : f'{token}',
        'protocol' : 'https',
        'username' : f'{username}',

    }
    html_template = render_to_string(email_template_name, parameters )
    subject = 'Registration Complete'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    message = EmailMessage(subject , html_template , email_from , recipient_list )
    message.content_subtype = 'html'
    message.send()



#After Mail Send Page
def token_send(request):
    if 'userid' in request.session:
        return redirect('/')
    else:
        return render(request , 'user/token_send.html')


#check Email verification
def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        user_obj = User.objects.filter(username = profile_obj.user.username).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/')
            profile_obj.is_verified = True
            profile_obj.save()
            user_obj.is_superuser = True
            user_obj.is_staff = True
            user_obj.is_active = True
            user_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/')
    except Exception as e:
        print(e)
        return redirect('/')

#for User Forgot Passward
# def forget_passward(request):
#     if request.method == 'POST':
#         password_form = PasswordResetForm(request.POST)
#         if password_form.is_valid():
#             data = password_form.cleaned_data['email']
#             user_email = User.objects.filter(Q(email=data))
#             user_obj = User.objects.filter(email = data).first()
#             profile_obj = Profile.objects.filter(user = user_obj ).first()
#             if user_email.exists():
#                 if profile_obj is None:
#                     messages.success(request, "Admin can't ")
#                     return redirect('/user/password-reset/')
#                 for user in user_email:
#                     subject = "Password Resquest"
#                     email_template_name = 'registration/password_reset_email-1.html'
#                     parameters = {
#                         'email' : user.email,
#                         'username' : user.username,
#                         'domain' : 'musicalclub.pythonanywhere.com',
#                         # 'site_name' : 'PostScribers',
#                         'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token' : default_token_generator.make_token(user) ,
#                         'protocol' : 'https',
#                     }
#                     try:
#                         message = render_to_string(email_template_name, parameters)
#                         email_from = settings.EMAIL_HOST_USER
#                         recipient_list = [user.email]
#                         email = EmailMessage(subject, message, email_from, recipient_list)
#                         email.content_subtype = "html"  # Main content is now text/html
#                         email.send()
#                     except Exception as e:
#                         print(e)
#                         return redirect('/user/password-reset/')
#                     # subject = 'Password Resquest'
#                     # email_template_name = 'registration/password_reset_email-1.html'
#                     # parameters = {
#                     #     'email' : user.email,
#                     #     'username' : user.username,
#                     #     'domain' : 'musicalclub.pythonanywhere.com',
#                     #     # 'site_name' : 'PostScribers',
#                     #     'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                     #     'token' : default_token_generator.make_token(user) ,
#                     #     'protocol' : 'https',
#                     # }
#                     # html_template = render_to_string(email_template_name, parameters)
#                     # try:
#                     #     subject = 'Reset Sassword'

#                     #     email_from = settings.EMAIL_HOST_USER
#                     #     recipient_list = [user.email]

#                     #     message = EmailMessage(subject , html_template , email_from , recipient_list )
#                     #     message.content_subtype = 'html'
#                     #     message.send()
#                     # except Exception as e:
#                     #     print(e)
#                     #     return redirect('/user/password-reset/')
#                     return render(request, 'user/password_reset_done.html')
#             else:
#                 messages.success(request, "Enter a valid email address.")
#                 return redirect('/user/password-reset/')
#     else:
#         password_form = PasswordResetForm()
#         try:
#             user2 = request.session.get('userid')
#             user_obj2 = User.objects.get(id=user2)
#         context = {
#             'total_price':total_price,
#             'cart_val':count,
#             'password_form' : password_form,
#     }
#     return render(request, 'user/password_reset_form.html', context)

