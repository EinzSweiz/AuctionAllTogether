from django.contrib.auth.mixins import LoginRequiredMixin

class UserLoggedIn(LoginRequiredMixin):
    login_url = 'account_login'
