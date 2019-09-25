# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _default_website(self):
        default_website_id = self.env.ref('website.default_website')
        return [default_website_id.id] if default_website_id else None

    website_ids = fields.Many2many('website', 'website_pricelist_rule_rel',
                                   'pricelist_id', 'website_id',
                                   string="website", default=_default_website,
                                   help='List of websites in which price-list '
                                        'will published.')


# class ProductPublicCategory(models.Model):
#     _inherit = "product.public.category"
#
#     def _default_website(self):
#         default_website_id = self.env.ref('website.default_website')
#         return [default_website_id.id] if default_website_id else None
#
#     website_ids = fields.Many2many('website', 'website_prod_public_categ_rel',
#                                    'website_id', 'category_id',
#                                    default=_default_website,
#                                    string='Websites', copy=False,
#                                    help='List of websites in which '
#                                         'category will published.')
#
#     @api.model
#     def create(self, vals):
#         tools.image_resize_images(vals)
#         res = super(ProductPublicCategory, self).create(vals)
#         # Multi-Website: Check different test-cases for child & parent category
#         if res.parent_id:
#             res.parent_id.write({
#                 'website_ids': [(4, website_id.id) for website_id in
#                                 res.website_ids]
#             })
#         return res
#
#     @api.multi
#     def write(self, vals):
#         tools.image_resize_images(vals)
#         res = super(ProductPublicCategory, self).write(vals)
#         # Multi-Website: Check different test-cases for child & parent category
#         if self.parent_id and self.website_ids.ids:
#             self.parent_id.write({
#                 'website_ids': [(4, website_id.id) for website_id in
#                                 self.website_ids]
#             })
#         if self.child_id:
#             for child_id in self.child_id:
#                 for website_id in child_id.website_ids:
#                     if website_id not in self.website_ids:
#                         child_id.write({
#                             'website_ids': [(3, website_id.id)]
#                         })
#         return res


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _default_website(self):
        default_website_id = self.env.ref('website.default_website')
        return [default_website_id.id] if default_website_id else None

    website_ids = fields.Many2many('website', 'website_prod_pub_rel',
                                   'website_id', 'product_id',
                                   string='Websites', copy=False,
                                   default=_default_website,
                                   help='List of websites in which '
                                        'Product will published.')
