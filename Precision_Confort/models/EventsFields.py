# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class EventsFields(models.Model):
    _inherit = "event.event"

    descrip = fields.Char(string="Description")
    image_id = fields.Binary(string='Image Event')
