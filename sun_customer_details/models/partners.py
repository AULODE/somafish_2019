from odoo import models, fields, api, _


class Partners(models.Model):
    _inherit = 'res.partner'
    
    tax_identification = fields.Char("Identifiant fiscal")
    trade_register = fields.Char("Registre de commerce")
    patent = fields.Char("Patente")
    ice = fields.Char("ICE")
    bank_name = fields.Char("Nom de la banque")
    agence = fields.Char("Agence")
    bank_address = fields.Char("Adresse")
    rib = fields.Char("RIB")
    

