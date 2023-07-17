# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import werkzeug

from odoo import http, SUPERUSER_ID

from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.addons.web.controllers.main import Session
from odoo.addons.website.controllers.main import Website as WebsiteHome
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class OAuthAutoLogin(OAuthLogin):
    def _autologin_disabled(self):
        return (
            "no_autologin" in http.request.params
            or "oauth_error" in http.request.params
            or "error" in http.request.params
        )

    def _autologin_link(self):
        providers = [p for p in self.list_providers() if p.get("autologin")]
        if len(providers) == 1:
            return providers[0].get("auth_link")

    @http.route()
    def web_login(self, *args, **kw):
        _logger.info(f"\n\n OAuthAutoLogin > web_login : %s %s\n\n" % (args, kw))
        response = super().web_login(*args, **kw)
        _logger.info(f"response %s" % (response))
        if not response.is_qweb:
            # presumably a redirect already
            return response
        if self._autologin_disabled():
            return response
        auth_link = self._autologin_link()
        if not auth_link:
            return response
        return werkzeug.utils.redirect(auth_link, 303)


class SessionLogout(Session):

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        '''
            Logout Session will work in combination
            with Lua access
        '''
        redirect = '/logout'
        return super(SessionLogout, self).logout(redirect=redirect)


class WebsiteHome(WebsiteHome):

    @http.route('/', type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):
        """ Autologin, if website app is installed """

        if not request.session.uid:
            return http.redirect_with_hash('/web/login')

        return super().index(**kw)
