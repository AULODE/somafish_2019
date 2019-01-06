from odoo import models, fields, api, _
import sys


class AccountPayment(models.Model):
    _inherit = "account.payment"
    
    discount_number = fields.Char("Numero de remise")
    check_number = fields.Char("Numero de chèque")
    
    credit_card_payment = fields.Char("N° STAN")
    bank_transfer_payment = fields.Char("SWIFT")
    is_bank = fields.Boolean("Bank")
    is_creditcc = fields.Boolean("credit")
    is_cheque = fields.Boolean("cheque")

    @api.onchange('journal_id')
    def _onchanges_journal(self):
        self.is_bank = self.is_creditcc = self.is_cheque = False
        if self.journal_id:
            self.currency_id = self.journal_id.currency_id or self.company_id.currency_id
            # Set default payment method (we consider the first to be the default one)
            payment_methods = self.payment_type == 'inbound' and self.journal_id.inbound_payment_method_ids or self.journal_id.outbound_payment_method_ids
            self.payment_method_id = payment_methods and payment_methods[0] or False
            # Set payment method domain (restrict to methods enabled for the journal and to selected payment type)
            payment_type = self.payment_type in ('outbound', 'transfer') and 'outbound' or 'inbound'
            if self.journal_id.journal_type_sel:
                if self.journal_id.journal_type_sel == 'is_bank':
                    self.is_bank = True
                elif self.journal_id.journal_type_sel == 'is_creditcc':
                    self.is_creditcc = True
                elif self.journal_id.journal_type_sel == 'is_cheque':
                    self.is_cheque = True

            return {'domain': {'payment_method_id': [('payment_type', '=', payment_type), ('id', 'in', payment_methods.ids)]}}
        return {}


class account_abstract_payment(models.AbstractModel):
    _inherit = "account.abstract.payment"

    journal_id = fields.Many2one('account.journal', string='Payment Method', required=True, domain=[('type', 'in', ('bank', 'cash'))])


class account_journal(models.Model):
    _inherit = 'account.journal'

    journal_type_sel = fields.Selection([('is_bank', 'Bank'),
                                     ('is_creditcc', 'Credit Card'),
                                     ('is_cheque', 'Cheque')
                                     ], string="Journal Type")

