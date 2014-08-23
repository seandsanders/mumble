# encoding: utf-8

from __future__ import unicode_literals

from web.auth import authenticated, user
from web.core import Controller, config

from brave.mumble.util import StartupMixIn
from brave.mumble.auth.controller import AuthenticationMixIn

import zxcvbn

log = __import__('logging').getLogger(__name__)


class RootController(Controller, StartupMixIn, AuthenticationMixIn):
    def index(self):
        if authenticated:
            return 'brave.mumble.template.index', dict()

        return 'brave.mumble.template.welcome', dict()
    
    def passwd(self, password):
        u = user._current_obj()
        
        #If the password has a score of less than 4, don't permit it (this check also done client-side)
        if(zxcvbn.password_strength(password).get("score") < int(config['mumble.required_pass_strength'])):
            return 'json:', dict(success=False, message="The password supplied was not strong enough.")

        try:
            u.password = password
            u.save()
        except:
            log.exception("Error attempting to assign password.")
            return 'json:', dict(success=False, message="Something terrible happened.")
        
        return 'json:', dict(success=True)
