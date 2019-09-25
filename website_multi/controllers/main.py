# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class Website(Website):

    @http.route()
    def get_switchable_related_views(self, key):
        views = request.env["ir.ui.view"].get_related_views(
            key, bundles=False).filtered(
            lambda v: v.customize_show and (
                v.website_id if v.website_id == request.website else None))
        return views.read(
            ['name', 'id', 'key', 'xml_id', 'arch', 'active', 'inherit_id'])
