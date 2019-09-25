# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.backend import WebsiteBackend


class WebsiteMultiBackend(WebsiteBackend):
    
    @http.route('', type="json", auth='user',
                website=True)
    def fetch_dashboard_data(self, date_from, date_to, website_id=None):
        results = super(WebsiteMultiBackend, self).fetch_dashboard_data(
            date_from, date_to)
        if not website_id:
            website_id = request.website.id
        results['website_ids'] = request.env['website'].search_read()
        results['website'] = request.env['website'].browse(website_id).domain
        results['current_website'] = request.website.domain
        return results
