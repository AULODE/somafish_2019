# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from uuid import uuid4

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class Website(models.Model):
    _inherit = "website"

    website_logo = fields.Binary("Website Logo")
    is_shop = fields.Boolean("Enable eCommerce ?")
