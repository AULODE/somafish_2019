# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
import calendar
import base64

from odoo import http, _
from odoo.http import request


class WebsitePrecisionComfort(http.Controller):

    @http.route([
        '/product_precision',
    ], type='http', auth="public", website=True, sitemap=False)
    def product_precision(self, **kw):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))

        product_ids = env['product.template'].sudo().search([], limit=3)

        if product_ids:
            return request.render("Precision_Confort.product_precision_confort", {
                'products': product_ids,
            })
        else:
            return request.redirect('/')

    @http.route(['/product_detail/<int:product>'], type='http', auth="public", website=True)
    def product_detail(self, product, **kw):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        product_id = env['product.template'].sudo().browse(product)
        if product_id:
            return request.render('Precision_Confort.product_detail', {
                'product': product_id,
            })
        else:
            return request.redirect('/product')

    @http.route([
        '/event_precision',
    ], type='http', auth="public", website=True, sitemap=False)
    def get_events_data(self, **kw):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))

        event_ids = env['event.event'].sudo().search([('state', '=', 'confirm')])
        today = datetime.today()
        actual_month = today.strftime("%B")
        actual_year = today.year
        dates = []
        events_recap =[]
        for event in event_ids:
            if event.date_begin:
                date_begin = datetime.strptime(event.date_begin, '%Y-%m-%d %H:%M:%S')
                #date = date_begin.day
                dates.append(str(date_begin.date()))
                events_recap.append(str(event.name) +'\n'+ str(date_begin.date()) +' - '+ str(datetime.strptime(event.date_end,'%Y-%m-%d %H:%M:%S').date()) + '\n' +str(event.address_id.name))
        # days = []
        # cal = calendar.Calendar()
        # for x in cal.itermonthdays(today.year, today.month):
        #     days.append(x)
        if event_ids:
            return request.render("Precision_Confort.event_precision", {
                'events_precision': event_ids,
                # 'month': actual_month,
                # 'year': actual_year,
                'dates': dates,
                #'calendar': days,
                'events_recap':events_recap,
            })
        else:
            return request.redirect('/')

    @http.route(['/events_detail/<int:event_precision>'], type='http', auth="public", website=True)
    def event_detail(self, event_precision):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
        event_id = env['event.event'].sudo().browse(event_precision)
        if event_id:
            return request.render('Precision_Confort.events_detail', {
                'event_precision': event_id,
            })
        else:
            return request.redirect('/event_precision')

    @http.route([
        '/store_locater',
    ], type='http', auth="public", website=True, sitemap=False)
    def home_page_precision(self, **kw):
        return request.render("Precision_Confort.store_locater")

    @http.route([
        '/testimonial',
    ], type='http', auth="public", website=True, sitemap=False)
    def testimonial_page_precision(self, **kw):

        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))

        testimonial_ids = env['testimonial'].sudo().search([('state', '=', 'confirmed')])

        if testimonial_ids:
            return request.render("Precision_Confort.testimonial", {
                'testimonials': testimonial_ids,
            })
        else:
            return request.redirect('/')

    @http.route('/testimonial/new', type='http', auth="public", methods=['POST'], website=True)
    def add_testimonial(self, **kwargs):
        vals = {
            'customer_name': request.params.get('name') or '',
            'customer_company': request.params.get('product') or '',
            'comment': request.params.get('review') or '',
            'state': 'draft',
        }
        if request.params.get('customFile'):
            attach = request.params.get('customFile').stream
            f = attach.read()
            vals['image_testimonials'] = base64.encodestring(f)
        request.env['testimonial'].sudo().create(vals)
        return request.redirect('/testimonial')

    @http.route('/subscribe/newsletter', type='http', auth="public", methods=['POST'], website=True)
    def subscribe(self, **kwargs):
        # """Send welcome email to subscribers."""
        template = request.env.ref('Precision_Confort.website_precision_confort').welcome_mail_template_id
        print ('template',template)
        if not template:
           return request.redirect('/')
        #Create contact
        contact = request.env["mail.mass_mailing.contact"].sudo().create(
            {'email':request.params.get('mail')}
        )
        # # Welcome new subscribers
        template.send_mail(
            contact.id,
            # Must send now to use context
            force_send=True,
            # If we cannot notify, the visitor shouldn't be bothered
            raise_exception=False,
        )
        return request.redirect('/')
