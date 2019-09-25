# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class Website(models.Model):
      _inherit = "website"

      testimonial_ids = fields.Many2many('testimonial',string="Les Testimonials",domain=[('state','=','confirmed')])
      welcome_mail_template_id = fields.Many2one(
            string="Welcome mail template",
            comodel_name='mail.template',
            ondelete='set null',
            help="Mail template to be sent when a contact is subscribed from "
                 "the website."
      )
