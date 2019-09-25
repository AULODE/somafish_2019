# -*- coding: utf-8 -*-

import logging
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request

_logger = logging.getLogger(__name__)

PPG = 20  # Products Per Page
PPR = 4   # Products Per Row


class CustomWebsiteSale(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        _logger.info('***** Accessing Website : %s - %s', request.website.id, request.website.name)
        return super(CustomWebsiteSale, self).shop(page=page, category=category, search=search, ppg=ppg, post=post)

    def _get_search_domain(self, search, category, attrib_values):
        domain = super(CustomWebsiteSale, self)._get_search_domain(search, category, attrib_values)
        categs = request.website.allowed_categ_ids
        brands = request.website.allowed_brand_ids
        if brands and categs:
            domain += ["|"]
        if categs:
            domain += [
                ('public_categ_ids', 'child_of', categs.ids),
            ]
        if brands:
            domain += [("brand_id", 'in', brands.ids)]
        return domain
