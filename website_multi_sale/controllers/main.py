# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    # def _get_search_domain(self, search, category, attrib_values):
    #     domain = super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)
    #     if not request.env.user.has_group('website.group_website_publisher'):
    #         domain += [('website_ids', 'in', request.website.id)]
    #     return domain

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        if not request.env.user.has_group('website.group_website_publisher') \
                and request.website.id not in product.website_ids.ids:
            return request.render('website.404')
        return super(WebsiteSale, self).product(product, category, search, **kwargs)
