# -*- coding: utf-8 -*-
from babel.dates import format_datetime
from odoo import http, fields, _
import logging
from odoo import fields, models, _
from odoo.http import Response
import json
from odoo import http
from odoo.http import request
from datetime import date, datetime, time, timedelta
from odoo.tools.safe_eval import safe_eval
_logger = logging.getLogger(__name__)

class Studentmoves(http.Controller):

    @http.route('/entry/read', methods=['post'], type='json', auth='public')
    def moves_read(self, **kw):
        
        params = json.loads(request.httprequest.data);
        journal_id = params['journal_id']
        from_date = params['from_date']
        to_date = params['to_date']
        type= params['type']
        
       

        
        
        _logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Sent batch %s',params )
        
        if type == 'entry':
           orders =  request.env['account.move'].sudo().search([('journal_id.id', '=', journal_id),('date', '>=', from_date),('date', '<=', to_date),('type', '=', type),('state', '=', 'posted')])
        
        
            
           if orders:
              list_of_result = []
              
              for rec in orders:
                result = {}
                _logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Sent batch %s',rec.name )
                result['name'] = rec.name
                result['type'] = rec.type
                result['ref'] = rec.ref
                result['user_id'] = rec.invoice_user_id.id
                #result['partner_name'] = rec.partner_id.name
                result['branch_id'] = rec.operating_unit_id.id
                result['branch'] = rec.operating_unit_id.name
                #result['partner_mobile'] = rec.partner_id.mobile
                #result['partner_area'] = rec.partner_id.area_id.name
                #result['partner_street'] = rec.partner_id.street
                #result['partner_city'] = rec.partner_id.city
                #result['partner_vat'] = rec.partner_id.vat
                #result['partner_tag'] = rec.partner_id.category_id.name[]



                result['date'] = rec.date
                result['journal_name']  = rec.journal_id.name
                result['journal_id']  = rec.journal_id.id
                result['move_lines'] = []
                for line in rec.line_ids:
                   line_data = {}
                   #line_data['product_id'] = line.product_id.id
                   #line_data['product_name'] = line.product_id.name
                   #line_data['product_categ'] = line.product_id.categ_id.id
                   #line_data['product_price'] = line.product_id.lst_price
                   line_data['debit'] = line.debit
                   line_data['credit'] = line.credit
                   line_data['account_id'] = line.account_id.id
                   line_data['branch_id'] = line.operating_unit_id.id
                   line_data['partner_id'] = line.partner_id.id or False
                   line_data['partner_name'] = line.partner_id.name or False
                   line_data['partner_mobile'] = line.partner_id.mobile
                   line_data['partner_area'] = line.partner_id.area_id.name
                   line_data['partner_street'] = line.partner_id.street
                   line_data['partner_city'] = line.partner_id.city
                   line_data['partner_vat'] = line.partner_id.vat
                   #line_data['partner_tag'] = line.partner_id.category_id.name
                   line_data['name'] = line.name
                   #line_data['product_uom_id'] = line.product_uom_id.id
                   #line_data['quantity'] = line.quantity
                   #line_data['discount'] = line.discount
                   result['move_lines'].append(line_data)
                list_of_result.append(result)

              return {
                    "success": {
                            "data": list_of_result
                    }
              
                }
           
        
           
           else:
              return {
                "error": {
                    "code": 1060,
                    "message": "Nomoves",
                }
             }             

 
        else:
            orders =  request.env['account.move'].sudo().search([('journal_id.id', '=', journal_id),('date', '>=', from_date),('date', '<=', to_date)])
            #lines =  request.env['account.move.line'].sudo().search([('move_id.ids', '=', orders.ids)])        