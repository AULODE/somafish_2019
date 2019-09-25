# -*- coding: ascii -*-

from odoo import api, fields, models, _


class View(models.Model):
    _inherit = "ir.ui.view"

    is_cloned = fields.Boolean(string='Cloned', copy=False, default=False,
                               help="This view is cloned"
                                    "(not present physically in file system) "
                                    "from default website's view for "
                                    "supporting multi-website feature.")

    # Multi Website: Automated Action On Create Rule
    ##################################################
    # If views are manually created for default website,
    # then it'll automatically cloned for other websites.
    #
    # As this method is also called when new website is created.
    # Because at the time of website creation ``Home`` page will be cloned,
    # So, this method will automatically triggered to
    # cloned all customize view(s).
    @api.model
    def multi_website_view_rule(self):
        default_website = self.env['website'].search([
            ('is_default_website', '=', True)])
        ir_model_data = self.env['ir.model.data']
        for website in self.env['website'].search(
                [('is_default_website', '=', False)]):
            for cus_view in self.search(
                    [('website_id', '=', default_website.id),
                     ('customize_show', '=', True),
                     ('is_cloned', '=', False),
                     '|', ('active', '=', False), ('active', '=', True)]):

                key = "%s_%s" % (cus_view.key, website.website_code)
                if not self.search(
                        [('key', '=', key), ('website_id', '!=', default_website.id),
                         '|', ('active', '=', False), ('active', '=', True)]):
                    new_cus_view = cus_view.copy({
                        'is_cloned': True,
                        'key': key,
                        'website_id': website.id
                     })

                    new_cus_vals = {}

                    inherited_key = "%s_%s" % (new_cus_view.inherit_id.key, website.website_code)
                    new_inherit_id = self.search(
                        [('key', '=', inherited_key),
                         '|', ('active', '=', False), ('active', '=', True)])
                    if new_cus_view.inherit_id and new_inherit_id:
                        new_cus_vals.update({
                            'inherit_id': new_inherit_id.id,
                        })
                    new_key = "%s_%s" % (cus_view.model_data_id.name, website.website_code)
                    model_data_id = ir_model_data.create({
                        'model': cus_view.model_data_id.model,
                        'name': new_key,
                        'res_id': new_cus_view.id,
                        'module': cus_view.model_data_id.module,
                    })
                    new_cus_view.write({
                        'model_data_id': model_data_id
                    })

    # Add the website_id to each customize QWeb view(s) at the time
    # of creation of new customize QWeb view(s).
    @api.model
    def create(self, values):
        # For Theme's View(s)
        if values.get('key') and values.get('type') == 'qweb' and \
                self.env.context.get('install_mode_data'):
            module_name = self.env.context['install_mode_data']['module']
            module_obj = self.env['ir.module.module'].sudo().search(
                [('name', '=', module_name)])
            if module_obj and \
                    (module_obj.category_id.name == 'Theme'
                     or (module_obj.category_id.parent_id
                         and module_obj.category_id.parent_id.name
                         == 'Theme')):
                values.update({
                    'website_id': module_obj.website_ids.id,
                })
        return super(View, self).create(self._compute_defaults(values))

    # Keep other website's view as it is when run server using -i/-u
    # As other website's views are not present anywhere in FS(file system).
    # So, once those are created/cloned from default website,
    # they can be changed/updated via debug mode only(ir.ui.view)
    # Menu: Settings/Technical/User Interface/Views
    #
    # Scenario 1:
    # -----------
    # For Delete those views, Manually set ``is_cloned`` field to ``False``
    # But Actually View is not deleted, It'll create again from
    # default website's view,
    # Find a way to delete website specific views form DB.
    #
    # Scenario 2:
    # -----------
    # If you write the code for already cloned views in FS(file system)/Module
    # to upgrade/update those views, then at the time of module update
    # process that cloned views id are found in FS(file system)/Module,
    # So in those particular views ``is_cloned`` will automatically
    # set to ``False`` (Definitely it'll be done from another method!!),
    # because now those views are not anymore cloned,
    # now they are physically present!!
    @api.multi
    def unlink(self):
        views = self.filtered(lambda v: not v.is_cloned)
        # Do not delete cloned view(s)
        # ----------------
        # 'View(s) that you want delete are '
        # 'cloned view(s).\n'
        # 'Cloned view(s) are automatically created '
        # 'for supporting multi website feature.\n'
        # 'If you still want to delete this view(s) '
        # 'then first Uncheck(set to False) the '
        # 'cloned field.\n'
        # 'By deleting cloned view(s) multi website '
        # 'will not work properly.\n'
        # 'So, Be sure before deleting view(s).'
        return super(View, views).unlink()
