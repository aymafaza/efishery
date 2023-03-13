from odoo import http
import json
from odoo.http import request
import jwt

class Authentication(http.Controller):
    @http.route('/sale-order', type='json', auth="public", methods=['POST'], csrf=False)
    def create_sale_order(self, **params):
        api_key = request.httprequest.headers.get("Authorization")
        token = api_key.split(" ")
        decoded = jwt.decode(token[1], "PLACE_SECRET_HERE_SOON", algorithms="HS256")
        
        partner_id = params.get("partner_id")
        orderline = params.get("orderline")

        # Create Sale Order
        order = request.env['sale.order'].create({
            'partner_id': partner_id,
            'order_line': [(0, 0, {'name': line.get('name'), 'product_id': line.get('id'), 'product_uom_qty': line.get('qty'),
                                   'price_unit': line.get('price_unit')}) for line in orderline],
        })

        # Confirm order
        order.action_confirm()
        # Update qty delivered
        for line in order.order_line:
            line.qty_delivered = line.product_uom_qty
        
        # Create invoice
        payment = request.env['sale.advance.payment.inv'].with_context({
            'active_model': 'sale.order',
            'active_ids': [order.id],
            'active_id': order.id,
        }).create({
            'advance_payment_method': 'delivered'
        })
        payment.create_invoices()
        # Post Invoice
        for invoice in order.invoice_ids:
            invoice.action_post()

        # Create Payment
        # Create an invoice with a CABA tax using the same tax account and pay it
        pmt_wizard = request.env['account.payment.register'].with_context(active_model='account.move', active_ids=order.invoice_ids.ids).create({
        })
        pmt_wizard.action_create_payments()

        return order

    @http.route('/sale-order', type='json', auth="public", methods=['GET'], csrf=False)
    def get_sale_order(self):
        api_key = request.httprequest.headers.get("Authorization")
        token = api_key.split(" ")
        decoded = jwt.decode(token[1], "PLACE_SECRET_HERE_SOON", algorithms="HS256")

        # Create Sale Order
        order = request.env['sale.order'].search([])
        orders = []
        for rec in order:
            orders.append({'name':rec.name, 'customer':rec.partner_id.name, 'date':rec.date_order, 'total':rec.amount_total})
        return orders