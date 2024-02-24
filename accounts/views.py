from .forms import RegistrationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Account 
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# Create your views here.
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name'] 
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            

            username = email.split('@')[0]
            user = Account.objects.create(first_name=first_name , last_name= last_name,  email= email, username = username)
            user.set_password(password)
            user.phone_number = phone_number
            user.save()

            print(f'The email saved from the registration form is {email} and the password is {password}')


            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "please activate your account"
            message = render_to_string('accounts/account_verfication_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    } 

    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # print(f'{email} and {password}')

        # Authenticate user

        user = authenticate(email=email, password=password)
        user_object = Account.objects.get(email = email)
        print(f'The email queries is {user_object.email}:{email} with the password as {user_object.password}:{password}')
        # something = (email == user_object.email) and (user_object.password == password)
        print(f'But when using the autentication method. The result is: {user}')

        if user is not None:
            # User is authenticated, log them in
            auth.login(request, user)
            messages.success(request, 'You are successfully logged in')
            return redirect('dashboard')
        else:
            # Invalid credentials
            messages.error(request, 'Invalid credentials, Please try again.')
            return redirect('login')
    
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are successfully logged out')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

    return HttpResponse('reached activate function')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__exact = email)

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Reset your account password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, f'Password reset email has been sent to {email}')
            return redirect('login')

        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')



def resetpassword_validator(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link is expired')
        return redirect('login')




def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_passwowrd = request.POST['confirm_password']
        
        if password == confirm_passwowrd:
            # all good
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Passowrd is set succefully')
            return redirect('login')
        else: 
            # throw an error
            messages.error(request, 'Passwords dont match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')   