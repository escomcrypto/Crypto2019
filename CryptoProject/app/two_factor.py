#Two factor mixins authentication
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse


class TwoFactorMixin(UserPassesTestMixin):
    """description of class"""
    def test_func(self):
        user = self.request.user
        return (user.is_authenticated and "verified" in self.request.session)

    def get_login_url(self):
        if (self.request.user.is_authenticated()):
            return reverse('two_factor:new')
        else:
            return reverse('home')

