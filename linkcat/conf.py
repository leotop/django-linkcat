# -*- coding: utf-8 -*-

from django.conf import settings

PAGINATE_BY = getattr(settings, 'LINKCAT_PAGINATE_BY', 20)

GROUPS_CAN_POST_LINK = getattr(settings, 'LINKCAT_GROUPS_CAN_POST_LINK', ['linkcat_post'])

GROUPS_CAN_MODERATE = getattr(settings, 'LINKCAT_GROUPS_CAN_MODERATE', ['linkcat_moderation'])

languages = (
             ('en', 'English'),
             ('fr', 'Français'),
             )

LANGUAGES = getattr(settings, 'LINKCAT_LANGUAGES', languages)
DEFAULT_LANGUAGE = LANGUAGES[0][0]

