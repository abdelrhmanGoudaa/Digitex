from odoo import http
from odoo.http import request
import json
from odoo.http import Response
from odoo.exceptions import AccessDenied
from odoo import SUPERUSER_ID

class Test(http.Controller):

    @http.route(route='/testing',type='json',auth='public',methods=['POST'],csrf=False)
    def test(self,**kw):
        data = kw.copy()
        print('kw',kw)
        print(data)
        data = request.httprequest.data.decode()
        print(data)
        print('INside TEsting')
        user = request.env['res.users'].with_user(SUPERUSER_ID).search([('login','=','admin')]) 
        print(user)
        print(user.id,user.name)
        return 'testtt'


    @http.route('/user_login_test', methods=['POST'], type='json', auth='public', csrf=False)
    def user_login(self, **kw):
        request_body = {}
        if kw:
            request_body = kw.copy()
        elif request.httprequest.data:
            request_body = json.loads(request.httprequest.data)
            print(request_body)
        else:
         #  Response.status = "403"
            return {"code": 403, "status": "Forbidden!", "message": "Messing data!"}


        try:
            user_env = request.env['res.users']
            user = user_env.with_user(SUPERUSER_ID).search([('login', '=', request_body.get('username'))])
            print(SUPERUSER_ID)
            # Check if user exists
            if not user:
             #  Response.status = "400"
               return {"code": 401, "message": " Username or Password is incorrect"}
            user_env.with_user(user)._check_credentials(password=request_body.get('password'),
                    user_agent_env={'interactive': False})

            return {
                "id": user.id,
                "name": user.partner_id.name,
                "username": user.login,
                "Employee_postition": user.employee_id.job_id.name or '',
                "employee_birthdate": user.employee_id.birthday  or '',
                "employee_email": user.employee_id.work_email or '',
                "start_date": getattr(user.employee_id,'start_date','No attribute start date') ,
                "location_long": getattr(user.employee_id.work_location_id,'longitude','No attribute longitude'),
                "location_lat": getattr(user.employee_id.work_location_id,'latitude','No attribute latitude') 
            }
        except AccessDenied as e:
    
              return {"code": 401, "message": f" access denied Username or Password is incorrect {e}"}


    @http.route('/user_all_event_test', methods=['POST'], type='json', auth='public')
    def user_all_event(self, **kw):
        # _logger.info('user_login')
        # api user employee attendence
        params = json.loads(request.httprequest.data);
        username =  params['username']
        date =  params['date'] or False
        datedaystart = date + ' 00:00:00'
        datedayend = date + ' 23:59:59'

       
        if not date:
            user = request.env['res.users'].sudo().search([('login', '=', username)])
            if user:
           # employee = request.env['hr.employee'].sudo().search([('user_id', '=', username)])
                event = request.env['calendar.event'].sudo().search([('partner_ids', 'in', user.partner_id.id)])
                if event:
                    list_of_result = []
                    for rec in event:
                        result = {}
                        result['start_date'] = rec.start
                        result['end_date'] = rec.stop
                        result['subject'] = rec.name
                        result['desc'] = rec.description or ''
                        result['location'] = rec.location or ''
                        result['duration'] = rec.duration
                        list_of_result.append(result)
                    return {"code": 200, "message": "Available events", "data": list_of_result}
               
                else:
                 #  Response.status = "400"
                   return {"code": 401, "message": "no event found"}
            else:

                return json.dumps({'status': 'fail', 'message': 'Invalid Username'})
        if date:
            user = request.env['res.users'].sudo().search([('login', '=', username)])
            if user:
           # employee = request.env['hr.employee'].sudo().search([('user_id', '=', username)])
                event = request.env['calendar.event'].sudo().search([('partner_ids', 'in', user.partner_id.id), ('start', '>=', datedaystart), ('start', '<=', datedayend)])
                if event:
                    list_of_result = []
                    for rec in event:
                        result = {}
                        result['start_date'] = rec.start
                        result['end_date'] = rec.stop
                        result['subject'] = rec.name
                        result['desc'] = rec.description or ''
                        result['location'] = rec.location or ''
                        result['duration'] = rec.duration
                        list_of_result.append(result)
                    return {"code": 200, "message": "Available events", "data": list_of_result}
               
                else:
                #   Response.status = "400"
                   return {"code": 401, "message": "no event found"}
            else:

                return json.dumps({'status': 'fail', 'message': 'Invalid Username'})

    @http.route('/user_all_hreq_test', methods=['POST'], type='json', auth='public')
    def user_all_hreq(self, **kw):
        # _logger.info('user_login')
        # api user employee attendence
        params = json.loads(request.httprequest.data)
        username =  params['username']

        user = request.env['res.users'].sudo().search([('login', '=', username)])
        if user:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', username)])
            holiday = request.env['hr.leave'].sudo().search([('employee_id', '=', employee.id)])
            if holiday:
                list_of_result = []
                for rec in holiday:
                    result = {}
                    result['start_date'] = rec.request_date_from
                    result['end_date'] = rec.request_date_to
                    result['reason'] = rec.name
                    result['type'] = rec.holiday_status_id.name
                    result['status'] = rec.state
                    list_of_result.append(result)
                return {"code": 200, "message": "Holiday request successfully", "data": list_of_result}
                
            else:
              #  Response.status = "400"
                return {"code": 401, "message": "no holiday request found"}
        else:

            return json.dumps({'status': 'fail', 'message': 'Invalid Username'})
    @http.route('/user_attendence_in_test', methods=['POST'], type='json', auth='public')
    def user_check_in(self, **kw):
        # _logger.info('user_login')
        # api user employee attendence
        params = json.loads(request.httprequest.data);
        print(params)
        print(params.get('username'))
        username =  params['username']
        check_in =  params['check_in']
        location_lat =  params['location_lat']
        location_long =  params['location_long']
        geolocation = location_lat + ',' + location_long


        user = request.env['res.users'].sudo().search([('login', '=', username)])
        print(geolocation)

        if user:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
            
            if check_in:
            #     old_attendence = request.env['hr.attendance'].sudo().search(
            #         [('employee_id', '=', employee.id), ('check_out', '=', False)])
            #     if old_attendence:
            #         # Response.status = "400"
            #         print(old_attendence.check_in)
            #         return {"code": 401, "message": " You should check out before be able checkin again"}
                same_attendence = request.env['hr.attendance'].sudo().search([('check_in', '=', check_in), ('employee_id', '=', employee.id)])
                print(same_attendence)
                if same_attendence:
                    # Response.status = "400"
                    return {"code": 401, "message": " You have already checked in at this time same_attendence"}
                wrongtime = request.env['hr.attendance'].sudo().search([('check_out', '>', check_in), ('employee_id', '=', employee.id), ('check_out', '!=', False)])
                if wrongtime:
                    # Response.status = "400"
                    return {"code": 401, "message": " You have already checked in at this time wrongtime"}
                else:
                  attendence = request.env['hr.attendance'].sudo().create({
                    'employee_id': employee.id,
                    'geo_check_in': geolocation,
                    'check_in': check_in
                   })
                  if not attendence:
                    #   Response.status = "400"
                      return {"code": 401, "message": " Check in failed"}
                  if attendence:
                    #   Response.status = "200"
                      return {"code": 200, "message": " Check in successfully"}
                  else:
                    #   Response.status = "400"
                      return {"code": 401, "message": " Check in failed"}
                
        else:

            return json.dumps({'status': 'fail', 'message': 'Invalid Username'})
