import logging
import string
import random
from hashlib import sha256

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, CreateView

from . import utils
from .forms import CustomUserCreationForm, LoginForm, ForgetPasswordForm, ForgetPasswordCodeForm
from .models import CustomUser
from django_project.settings import SECRET_KEY
from django_project import settings

logger = logging.getLogger(__name__)


def generate_verification_code():
    return ''.join(random.sample(string.digits, 5))


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'account/registration_form.html'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(False)
            user.is_active = False
            user.source = 'Register'
            user.save(True)

            if settings.DEBUG:
                site = '127.0.0.1:8000'
            else:
                site = Site.objects.get_current()

            path = reverse('account:result')
            url = "http://{site}{path}?type=validation&id={id}&sign={sign}".format(
                site=site, path=path, id=user.id, sign=sha256(SECRET_KEY + user.id))

            content = """
                            <p>Подтвердите email</p>

                            <a href="{url}" rel="bookmark">{url}</a>

                            <br />
                            Или перейдите по ссылке, чтобы подтвердить email.
                            {url}
                            """.format(url=url)
            send_mail(
                recipient_list=[
                    user.email,
                ],
                subject='Подтверждение почты',
                message=content,
                from_email=settings.EMAIL_HOST
            )

            url = reverse('accounts:result') + '?type=register&id=' + str(user.id)
            return HttpResponseRedirect(url)
        else:
            return self.render_to_response({'form': form})


class LogoutView(RedirectView):
    url = '/login/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = '/'
    redirect_field_name = REDIRECT_FIELD_NAME
    login_ttl = 2626560

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        kwargs['redirect_to'] = redirect_to

        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
            logger.info(self.redirect_field_name)

            auth.login(self.request, form.get_user())
            if self.request.POST.get("remember"):
                self.request.session.set_expiry(self.login_ttl)

            return super(LoginView, self).form_valid(form)

        else:
            return self.render_to_response({
                'form': form
            })

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)

        if not url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=[self.request.get_host()]):
            redirect_to = self.success_url

        return redirect_to


def account_result(request):
    type = request.GET.get('type')
    id = request.GET.get('id')

    user = get_object_or_404(get_user_model(), id=id)
    logger.info(type)
    if user.is_active:
        return HttpResponseRedirect('/')
    if type and type in ['register', 'validation']:
        if type == 'register':
            content = '''
    На ваш адрес электронной почты было отправлено письмо с подтверждением. Пожалуйста, подтвердите свой адрес электронной почты.
    '''
            title = 'Вы успешно зарегистрировались'
        else:
            c_sign = sha256(settings.SECRET_KEY + str(user.id))
            sign = request.GET.get('sign')
            if sign != c_sign:
                return HttpResponseForbidden()

            user.is_active = True
            user.save()
            content = '''
            Вы подтвердили электронную почту
            '''
            title = 'Проверка прошла успешно'
        return render(request, 'account/result.html', {
            'title': title,
            'content': content
        })
    else:
        return HttpResponseRedirect('/')


class ForgetPasswordView(FormView):
    form_class = ForgetPasswordForm
    template_name = 'account/forget_password.html'

    def form_valid(self, form):
        if form.is_valid():
            blog_user = CustomUser.objects.filter(email=form.cleaned_data.get("email")).get()
            blog_user.password = make_password(form.cleaned_data["new_password2"])
            blog_user.save()
            return HttpResponseRedirect('/login/')
        else:
            return self.render_to_response({'form': form})


class ForgetPasswordEmailCode(CreateView):

    def post(self, request, *args, **kwargs):
        form = ForgetPasswordCodeForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Неправильный адрес электронной почты")
        to_email = form.cleaned_data["email"]

        code = generate_verification_code()
        utils.send_verify_email(to_email, code)
        utils.set_code(to_email, code)

        return HttpResponse("ok")
