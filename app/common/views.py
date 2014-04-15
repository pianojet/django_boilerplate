from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse

from app.common.forms import LoginForm, SignupForm
from ufe.common.login_required.decorator import login_not_required

def index(request):
    return render(request, 'common/index.html', {})

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

@login_not_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('common_home'))


@login_not_required
def signup(request):
  """
  Create a login for a new customer.  
  """

  form = SignupForm()

  if request.POST:
    form = SignupForm(request.POST)
    if form.is_valid():
      u = User()
      u.email = form.cleaned_data['email']
      u.set_password(form.cleaned_data['password'])
      u.save()
      return HttpResponseRedirect(reverse('common_login'))

  return render_auth(request, 'create_customer_login.html', {'Customer' : lCustomer,
                                                             'form' : lForm})