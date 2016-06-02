# -*- coding: utf-8 -*-


def get_slide(screen, screen_width):
    if screen_width >= screen.xl_breakpoint:
        image = screen.image_xl
        html = screen.html_xl
    if screen_width >= screen.lg_breakpoint and screen_width < screen.xl_breakpoint:
        image = screen.image_lg
        html = screen.html_lg
    if screen_width >= screen.md_breakpoint and screen_width < screen.lg_breakpoint:
        image = screen.image_md
        html = screen.html_md
    if screen_width >= screen.sm_breakpoint and screen_width < screen.md_breakpoint:
        image = screen.image_sm
        html = screen.html_sm
    if screen_width >= screen.xs_breakpoint and screen_width < screen.sm_breakpoint:
        image = screen.image_xs
        html = screen.html_xs
    if screen_width > screen.xxs_breakpoint and screen_width < screen.xs_breakpoint:
        image = screen.image_xxs
        html = screen.html_xxs
    if screen_width > screen.xxxs_breakpoint and screen_width < screen.xxs_breakpoint:
        image = screen.image_xxs
        html = screen.html_xxs
    if screen_width <= screen.xxxs_breakpoint:
        image = screen.image_xxxs
        html = screen.html_xxxs
    return (image, html)