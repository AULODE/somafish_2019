# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request


class TestImonial(models.Model):
    _name = "testimonial"

    comment = fields.Char(string="Testimonials")
    image_testimonials = fields.Binary()
    customer_name = fields.Char(string="Name")
    customer_company = fields.Char(string="Company")
    state = fields.Selection([('draft','Brouillon'),('confirmed','Confirmé')],string="Status",default='draft')

    @api.multi
    def confirm_testimonial(self):
        self.state = 'confirmed'
