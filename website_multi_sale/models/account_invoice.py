# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    website_id = fields.Many2one('website', string="Website")


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    individual_invoice = fields.Boolean("Create Splitted Invoice", 
        help="Tick if you want to create individual invoices from the sale order")

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(order,
                                                                 so_line,
                                                                 amount)

        res.website_id = order.website_id

        return res
