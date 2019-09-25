# -*- coding: utf-8 -*-

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    allowed_categ_ids = fields.Many2many('product.public.category', string='Allowed eCommerce Categories')
    allowed_brand_ids = fields.Many2many("product.brand", string="Allowed Brands")
