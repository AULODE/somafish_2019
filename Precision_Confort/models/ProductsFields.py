# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class ProductsFields(models.Model):
    _inherit = "product.template"

    description_general = fields.Char(string="Description general")
    features_and_benefits = fields.Char(string='Features and Benefits')
    images_ids = fields.Many2many('ir.attachment', string='Images gallery')
    images = fields.Binary()
    img = fields.Binary(string='Images Product')
    img_detail = fields.Binary(string='Image detail')
    downloads = fields.Many2many('ir.attachment','ir_attachment_download','down_1','down2', string='Downloads')
    specifications = fields.Char(string='Specifications')

    @api.model
    def create(vals):
        product=super(ProductsFields).create(vals)
        for attach in product.downloads:
            attach.public = True
        return product

    @api.multi
    def write(self, vals):
        product = super(ProductsFields, self).write(vals)
        print ('hhhhhh')
        for attach in self.downloads:
            attach.public = True

        return product


