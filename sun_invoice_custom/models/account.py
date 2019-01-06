import math

from odoo import models, fields, api, _
from odoo.tools import  float_round
from odoo.exceptions import UserError, ValidationError
from num2words import num2words

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.depends('amount_total')
    def _get_amount_words(self):
        for inv in self:
            if inv.amount_total:
                check_amount_in_words = num2words(inv.amount_total, lang='fr')
                check_amount_in_words = check_amount_in_words.split("virgule")[0]
                decimals = inv.amount_total % 1
                if decimals >= 10**-2:
                    last_words = int(round(float_round(decimals*100, precision_rounding=1)))
                    last_words = num2words(last_words, lang='fr')
                    currency_words = _(' %s') % str(inv.currency_id.symbol)
                    check_amount_in_words += currency_words +' virgule '+last_words + _(' centimes')
                else:
                    currency_words = _(' %s') % str(inv.currency_id.symbol)
                    check_amount_in_words += currency_words
                inv.amount_words = check_amount_in_words

    amount_words = fields.Char("Amount In Words Total",compute="_get_amount_words")


class Account_journal(models.Model):
    _inherit = 'account.journal'

    @api.model
    def _update_custom_sequence_name(self):
        for jrnl in self.search([('type', '=', 'sale')]):
            if jrnl.sequence_id:
                jrnl.sequence_id.prefix = "BL-FACTURE/%(range_year)s/"
            if jrnl.refund_sequence_id:
                jrnl.refund_sequence_id.prefix = "AVOIR/%(range_year)s/"