# -*- coding: utf-8 -*-

from linkcat.conf import GROUPS_CAN_MODERATE, GROUPS_CAN_POST_LINK


def is_moderator(user):
    is_moderator = False
    if not user.is_anonymous():
        if user.is_superuser:
            is_moderator = True
        else:
            is_moderator = user.groups.filter(name__in=GROUPS_CAN_MODERATE).exists()
    return is_moderator

def can_post_link(user):
    is_moderator = False
    if not user.is_anonymous():
        if user.is_superuser:
            is_moderator = True
        else:
            is_moderator = user.groups.filter(name__in=GROUPS_CAN_POST_LINK).exists()
    return is_moderator