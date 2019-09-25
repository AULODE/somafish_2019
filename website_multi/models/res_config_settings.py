# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, Warning

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_theme_id = fields.Many2one(
        'ir.module.module', string='Theme',
        related='website_id.website_theme_id',
        help='Choose theme for current website.')

    # Unique theme per Website for now ;)
    # Do enable support for same theme in multiple website
    @api.onchange('website_theme_id')
    def onchange_theme_id(self):
        if (self.website_id.id not in self.website_theme_id.website_ids.ids) \
                and (self.website_theme_id and
                     self.website_theme_id.website_ids):
            warning = {
                'title': 'Warning',
                'message': _('Selected theme is already active in '
                             'different website.')}
            self.website_theme_id = False
            return {'warning': warning}

    @api.model
    def _get_classified_fields(self):
        res = super(ResConfigSettings, self)._get_classified_fields()
        if 'website_theme_id' in dir(self):
            ir_module = self.env['ir.module.module']
            install_theme_lst = []
            uninstall_theme_lst = []
            install_theme_lst.append(self.website_theme_id)
            theme_un = ir_module.sudo().search(
                ['|', ('category_id.name', '=', 'Theme'),
                 ('category_id.parent_id.name', '=', 'Theme')]
            )
            for theme in theme_un:
                if not theme.website_ids and len(theme.website_ids.ids) < 1:
                    uninstall_theme_lst.append(theme)
            res.update({
                'install_theme': install_theme_lst,
                'uninstall_theme': uninstall_theme_lst
            })
        return res

    # Overriding Method
    @api.multi
    def execute(self):
        self.ensure_one()

        # Multi Website: Do not allow more than 1 website as default website
        if self.env['website'].search_count(
                [('is_default_website', '=', True)]) > 1:
            raise Warning(
                _('You can define only one website as default one.\n'
                  'More than one websites are not allowed '
                  'as default website.'))

        if not self.env.user._is_superuser() and not \
                self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only administrators can change the settings"))

        self = self.with_context(active_test=False)
        classified = self._get_classified_fields()

        # default values fields
        IrDefault = self.env['ir.default'].sudo()
        for name, model, field in classified['default']:
            if isinstance(self[name], models.BaseModel):
                if self._fields[name].type == 'many2one':
                    value = self[name].id
                else:
                    value = self[name].ids
            else:
                value = self[name]
            IrDefault.set(model, field, value)

        # group fields: modify group / implied groups
        for name, groups, implied_group in classified['group']:
            if self[name]:
                groups.write({'implied_ids': [(4, implied_group.id)]})
            else:
                groups.write({'implied_ids': [(3, implied_group.id)]})
                implied_group.write({'users': [(3, user.id) for user in
                                               groups.mapped('users')]})

        # other fields: execute method 'set_values'
        # Methods that start with `set_` are now deprecated
        for method in dir(self):
            if method.startswith('set_') and method is not 'set_values':
                _logger.warning(_('Methods that start with `set_` '
                                  'are deprecated. Override `set_values` '
                                  'instead (Method %s)') % method)
        self.set_values()

        # module fields: install/uninstall the selected modules
        to_install = []
        to_upgrade = self.env['ir.module.module']
        to_uninstall_modules = self.env['ir.module.module']
        lm = len('module_')
        for name, module in classified['module']:
            if self[name]:
                to_install.append((name[lm:], module))
            else:
                if module and module.state in ('installed', 'to upgrade'):
                    to_uninstall_modules += module

        if 'install_theme' in classified and 'uninstall_theme' in classified:
            for theme in classified['install_theme']:
                if theme:
                    to_install.append((theme.name, theme))
                if theme.state == 'installed':
                    to_upgrade += theme
            for theme in classified['uninstall_theme']:
                if theme and theme.state in ('installed', 'to upgrade'):
                    to_uninstall_modules += theme

        if to_uninstall_modules:
            to_uninstall_modules.button_immediate_uninstall()

        if to_upgrade:
            to_upgrade.button_immediate_upgrade()

        self._install_modules(to_install)

        if to_install or to_uninstall_modules:
            # After the uninstall/install calls, the registry and environments
            # are no longer valid. So we reset the environment.
            self.env.reset()
            self = self.env()[self._name]

        # pylint: disable=next-method-called
        config = self.env['res.config'].next() or {}
        if config.get('type') not in ('ir.actions.act_window_close',):
            return config

        # force client-side reload (update user menu and current view)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
