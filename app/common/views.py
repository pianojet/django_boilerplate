from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout

from app.common.forms import LoginForm

def home(request):
    return render(request, 'common/home.html', {})

def login(request):
    message = ""
    next_url = request.GET.get("next", str(getattr(settings, 'LOGIN_REDIRECT_URL', '/')))
    if request.POST:
        email = request.POST['username']
        password = request.POST['password']
        form = LoginForm(data={"username": email, "password": password})
        # get the ip address for the auth_log
        try:
            address = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            address = request.META['REMOTE_ADDR']
        if form.is_valid():
            try:
                user = authenticate(username=form.data['username'], password=form.data['password'])
            except:
                user = None
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    message += "You're successfully logged in!"
                    user_profile = UserProfile.objects.get(user=request.user)
                    return HttpResponseRedirect(next_url)
                else:
                    message += "Your account is not active, please contact the site admin."
            else:
                message += "Your username and/or password were incorrect."

    else:
        form = LoginForm()

    return render(request, 'common/login.html', {'form': form, 'message': message})