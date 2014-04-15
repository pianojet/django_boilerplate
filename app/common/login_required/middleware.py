from re import compile as recompile
import json
from urlparse import parse_qs

from django.conf import settings
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


# Modified version of https://github.com/sdelements/django-security/blob/master/security/middleware.py, which was modified from
# Ryan Witt http://onecreativeblog.com/post/59051248/django-login-required-middleware

# Copyright (c) 2008, Ryan Witt
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the organization nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class LoginRequiredMiddleware(object):
    """
    Middleware that requires a user to be authenticated to view any page on
    the site that hasn't been white listed. Exemptions to this requirement
    can optionally be specified in settings via a list of regular expressions
    in LOGIN_EXEMPT_URLS (which you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.

    Accounts for both internal api_key authentication as well as
    OAuth access_token authentication.

    """
    EXEMPT_URLS = [recompile(str(settings.LOGIN_URL))]
    if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
        EXEMPT_URLS += [recompile(str(expr)) for expr in settings.LOGIN_EXEMPT_URLS]

    # def return_api_forbidden(self, message=None):
    #     try:
    #         from djangorestframework.permissions import _403_FORBIDDEN_RESPONSE
    #         response = _403_FORBIDDEN_RESPONSE.response.raw_content
    #     except Exception as inst:
    #         response = {"denied": "You do not have permission to access this resource. You may need to login or otherwise authenticate the request."}
    #         if message is not None and message != "":
    #             response.update({"detail": message})
    #     return HttpResponseForbidden(json.dumps(response), mimetype="application/json")

    def return_need_auth(self, request, view, args, kwargs):
        # if request.is_ajax():
        #     return self.return_api_forbidden()
        # else:
        return login_required(view)(request, args, kwargs)

    def process_view(self, request, view, *args, **kwargs):
        if hasattr(request, 'user') and request.user.is_authenticated():
            pass  # user is logged in, no further checking required
        # elif any(url in request.path_info for url in LoginRequiredMiddleware.API_URLS):
        #     try:
        #         username, api_key, auth_type = self.extract_credentials(request)
        #         user = APITokenBackend().authenticate(username, api_key, auth_type)
        #         # get the ip address for the auth_log
        #         try:
        #             address = request.META['HTTP_X_FORWARDED_FOR']
        #         except KeyError:
        #             address = request.META['REMOTE_ADDR']
        #         if user:
        #             request.user = user
        #         else:
        #             raise ValueError("Invalid credentials")
        #     except (ValueError, OAuthExpired) as inst:
        #         return self.return_api_forbidden(message=inst)
        elif hasattr(request, 'user') and not request.user.is_authenticated():
            if not (getattr(view, 'login_exempt', False) or
                    any(m.match(request.path_info) for m in LoginRequiredMiddleware.EXEMPT_URLS)):
                return self.return_need_auth(request, view, args, kwargs)
        elif not hasattr(request, 'user'):
            raise Exception("The Login Required middleware requires authentication middleware to be installed.")

    # def extract_credentials(self, request):
    #     """ acquire authentication credentials for either internal api_key usage or OAuth """
    #     if request.method == 'POST' and request.POST.get('access_token'):
    #         username = None
    #         api_key = request.POST.get('access_token')
    #         auth_type = 'oauth'
    #     elif request.method == 'GET' and request.GET.get('access_token'):
    #         username = None
    #         api_key = request.GET.get('access_token')
    #         auth_type = 'oauth'            
    #     elif request.META.get('HTTP_AUTHORIZATION'):
    #         try:
    #             (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()
    #             auth_type = auth_type.strip().lower()
    #         except: # catch-all to reduce problems to an auth header error
    #             raise ValueError("Error reading authorization header.")

    #         # api_key - via Authorization header
    #         if auth_type in ('apitoken', 'apikey'):
    #             username, api_key = data.split(':', 1)
    #         # OAuth
    #         elif auth_type in ('bearer', 'oauth'):
    #             username = None # usage of oauth access_token does not require username
    #             api_key = data
    #         else:
    #             raise ValueError("Incorrect authorization header.")
    #     elif request.method in ('PUT', 'DELETE') and 'api_token' not in request.GET and 'api_token' not in request.POST:
    #         try:
    #             username = None
    #             api_key = parse_qs(request.body)['access_token'][0]
    #             auth_type = 'oauth'
    #         except: # catch-all to reduce problems to an access token error
    #             raise ValueError("Error reading access token.")

    #     else: # api_key - via query params
    #         username = request.GET.get('username') or request.POST.get('username', None)
    #         api_key = request.GET.get('api_token') or request.POST.get('api_token', None)
    #         auth_type = 'apitoken'
    #     return username, api_key, auth_type
