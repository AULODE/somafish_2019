# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from uuid import uuid4

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class Website(models.Model):
    _inherit = "website"

    is_default_website = fields.Boolean(string='Default Website', readonly=1)
    website_code = fields.Char(string='Website Code', readonly=0,
                               default=lambda self: uuid4().hex[:8],
                               help='Unique code per website.')
    website_theme_id = fields.Many2one('ir.module.module', string='Theme',
                                       help='Choose theme for current '
                                            'website.')
    menu_ids = fields.One2many("website.menu", "website_id", string="Menu", ondelete="cascade")
    page_ids = fields.One2many("website.page", "website_id", string="Pages", ondelete="cascade")

    _sql_constraints = [
        ('domain_uniq', 'unique(domain)', 'Domain name already exists !'),
    ]

    # ----------------------------------------------------------
    # Multi Website
    # ----------------------------------------------------------
    @api.multi
    def write(self, values):
        self._get_languages.clear_cache(self)
        if values.get('website_code') or \
                (values.get('is_default_website')
                 and self != self.env.ref('website.default_website')):
            raise Warning(_('Unexpected bad things will happen!\n'
                            'Changing website code or default website '
                            'can have unintended side effects.\n'
                            '- We will not updated your old views.\n'
                            '- If above action is not properly done '
                            'then it will break your current '
                            'multi website feature.'))
        return super(Website, self).write(values)

    @api.model
    def create(self, values):
        res = super(Website, self).create(values)

        default_website = self.env['website'].search([(
            'is_default_website', '=', True)])
        if not len(default_website) or len(default_website) > 1:
            raise Warning(_('Either default website is not defined '
                            'or multiple default website is defined!!\n'
                            'You can define only one website as '
                            'default website.'))

        website_menu = self.env['website.menu']
        ir_model_data = self.env['ir.model.data']

        # Menu Entries:
        # Clone top menu & home menu of default website for new website
        top_menu = self.env.ref('website.main_menu', False)
        home_menu = self.env.ref('website.menu_homepage', False)
        new_home_menu = False
        if top_menu and home_menu:
            top_menu = website_menu.search([
                ('id', '=', self.env.ref('website.main_menu').id),
                ('website_id', '=', default_website.id)])
            home_menu = website_menu.search([
                ('id', '=', self.env.ref('website.menu_homepage').id),
                ('website_id', '=', default_website.id)])
            new_top_menu = top_menu.copy()
            new_top_menu.write({
                'website_id': res.id,
            })
            new_home_menu = home_menu.copy()
            new_home_menu.write({
                'website_id': res.id,
                'parent_id': new_top_menu.id,
            })

        # Home Page & View Entry:
        # Clone home page & view of default website for new website
        home_page = self.env.ref('website.homepage_page', False)
        if home_page and new_home_menu:
            new_home_page = home_page.copy()

            new_home_page.view_id.write({
                'name': home_page.view_id.name,
                'website_id': res.id,
                'key': home_page.view_id.key + '_' + res.website_code,
                'is_cloned': True,
            })

            home_model_data_id = ir_model_data.create({
                'model': home_page.view_id.model_data_id.model,
                'name': home_page.view_id.model_data_id.name +
                        '_' + res.website_code,
                'res_id': new_home_page.view_id.id,
                'module': home_page.view_id.model_data_id.module,
            })
            new_home_page.view_id.write({
                'model_data_id': home_model_data_id
            })

            new_home_page.write({
                'url': home_page.url,
                'view_id': new_home_page.view_id.id,
                'website_published': True,
                'website_ids': [(6, 0, [res.id])],
                'menu_ids': [(6, 0, [new_home_menu.id])],
            })
        return res


class Menu(models.Model):
    _inherit = "website.menu"

    website_id = fields.Many2one('website', 'Website', required=True,
                                 default=lambda self: self.env.ref('website.default_website'))  # TODO: support multiwebsite once done for ir.ui.views
    parent_id = fields.Many2one('website.menu', 'Parent Menu', index=True,
                                ondelete="cascade",
                                domain="[('website_id','=', website_id)]")
    menu_view = fields.Many2one('ir.ui.view', domain=[('type', '=', 'qweb')],
                                string='Menu View')
