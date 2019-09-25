# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    website_id = fields.Many2one('website', string='Website',
                                 help='Website reference for quotation/order.')

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['website_id'] = self.website_id.id
        return res
