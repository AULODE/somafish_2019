
from odoo import models, api, fields, _
from odoo.tools import formatLang


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def get_proper_format(self, amount):
        number = formatLang(self.env, amount, monetary=True, currency_obj=self.currency_id)
        return number.rstrip('0').rstrip('.').replace('.00', '')

    @api.multi
    def get_datad(self):
        list = []
        total_final = 0.0
        for line in self.order_line:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_id)
            name_list = []
            stringname = ''
            for rec in line.product_id.attribute_value_ids:
                stringname += ' ' + rec.name
            name_list.append({'1': line.product_id.name + stringname})
#             for pro in line.product_id.bom_products:
#                 name_list.append({'1': str(pro.product_qty)+ " "+pro.product_uom.name + " - "+ pro.product_id.name})
            unit_price = price + (line.price_tax / line.product_uom_qty)
            unit_price = round(unit_price, 2) 
            list.append({'unit_price':unit_price, 'name':name_list, 'qty':line.product_uom_qty,
              'product_uom':line.product_uom.name, 'price_subtotal':unit_price * line.product_uom_qty})
        return list

    @api.multi
    def get_datass(self):
        listss = []
        total_final = 0.0
        for line in self.order_line:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_id)

            unit_price = price + (line.price_tax / line.product_uom_qty)
#             list.append({'unit_price':unit_price,'name':line.name,'qty':line.product_uom_qty,
#               'product_uom':line.product_uom.name,'price_subtotal':unit_price*line.product_uom_qty})
            total_final += unit_price * line.product_uom_qty
        total_final = round(total_final)    
        listss.append({'total_final':total_final})
        return listss


class ResCompany(models.Model):
    _inherit = "res.company"

    instruction = fields.Html("Instruction")
    terms_condition = fields.Html("Terms and Condition")
