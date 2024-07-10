# -*- coding: utf-8 -*-

from odoo import _, http
from odoo.exceptions import ValidationError

from odoo.addons.website_sale.controllers import main

class WebsiteSale(main.WebsiteSale):

    def _get_shop_payment_values(self, order, **kwargs):
        res = {}
        res['on_payment_step'] = True

        if order.fiscal_position_id.is_taxcloud:
            try:
                order.validate_taxes_on_sales_order()
            except ValidationError:
                res.setdefault('errors', []).append((_("Validation Error"), _("This address does not appear to be valid. Please make sure it has been filled in correctly.")))

        res.update(super(WebsiteSale, self)._get_shop_payment_values(order, **kwargs))
        return res

class PaymentPortal(main.PaymentPortal):

    @http.route()
    def shop_payment_transaction(self, order_id, access_token, **kwargs):
        """
        Recompute taxcloud sales before payment
        """
        order = http.request.website.sale_get_order()
        order.validate_taxes_on_sales_order()

        return super().shop_payment_transaction(order_id, access_token, **kwargs)
