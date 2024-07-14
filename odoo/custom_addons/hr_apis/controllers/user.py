import re
from babel.dates import format_datetime
from odoo import http, fields, _
import logging
from odoo import fields, models, _
from odoo.http import Response
import hashlib
import json
from odoo import http
from odoo.http import request
from datetime import date, datetime, time, timedelta
from odoo.tools.safe_eval import safe_eval
from datetime import datetime
import json
import logging
from odoo import SUPERUSER_ID
from odoo.exceptions import AccessDenied
from odoo.http import Controller, Response, request, route

_logger = logging.getLogger(__name__)


class User(http.Controller):

    @http.route(route='/get_remaining_leaves', type='json', auth='public', methods=['POST'], csrf=False)
    def get_remaining_leaves(self):
        # get the user
        params = json.loads(request.httprequest.data)
        username = params.get('username')
        print(username)
        user = request.env['res.users'].sudo().search([('login', '=', username)])
        print(user)
        if user:
            user_id = user.id
            # get the employee related to the user
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)], limit=1)
            if employee:
                # get the leave data for the employee
                leave_data = request.env['hr.leave'].sudo().read_group(
                    [('employee_id', '=', employee.id)],
                    ['number_of_days', 'holiday_status_id'],
                    ['holiday_status_id']
                )
                
                # get leave types
                leave_types = {leave_type.id: leave_type.name for leave_type in request.env['hr.leave.type'].sudo().search([])}

                # format the data as specified
                res = {
                    "Paid Time Off": 0,
                    "Sick Time Off": 0,
                    "Parental Leaves": 0,
                    "Extra Hours": 0,
                    "Unpaid": 0,
                    "Compensatory Days": 0,
                    "Permission": 0
                }

                for leave in leave_data:
                    leave_type_name = leave_types.get(leave['holiday_status_id'][0])
                    if leave_type_name in res:
                        res[leave_type_name] += int(leave['number_of_days'])
                

                return {"code": 200, "message": "Available events", "data": res}
            else:
                return {"code": 401, "message": "No Such an Employee"}
        # for no user gotten
        return {"code": 401, "message": "No user Provided"}

    @http.route('/user_attendence_in', methods=['POST'], type='json', auth='public')
    def user_check_in(self, **kw):
        # _logger.info('user_login')
        # api user employee attendence
        params = json.loads(request.httprequest.data);
        username =  params['username']
        check_in =  params['check_in']
        location_lat =  params['location_lat']
        location_long =  params['location_long']
        geolocation = location_lat + ',' + location_long


        user = request.env['res.users'].sudo().search([('login', '=', username)])

        if user:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
            
            if check_in:
                old_attendence = request.env['hr.attendance'].sudo().search(
                    [('employee_id', '=', employee.id), ('check_out', '=', False)])
                if old_attendence:
                    Response.status = "400"
                    return {"code": 401, "message": " You have already checked in at this time"}
                same_attendence = request.env['hr.attendance'].sudo().search([('check_in', '=', check_in), ('employee_id', '=', employee.id)])
                if same_attendence:
                    Response.status = "400"
                    return {"code": 401, "message": " You have already checked in at this time"}
                wrongtime = request.env['hr.attendance'].sudo().search([('check_out', '>', check_in), ('employee_id', '=', employee.id), ('check_out', '!=', False)])
                if wrongtime:
                    Response.status = "400"
                    return {"code": 401, "message": " You have already checked in at this time"}
                else:
                  attendence = request.env['hr.attendance'].sudo().create({
                    'employee_id': employee.id,
                    'geo_check_in': geolocation,
                    'check_in': check_in
                   })
                  if not attendence:
                      Response.status = "400"
                      return {"code": 401, "message": " Check in failed"}
                  if attendence:
                      Response.status = "200"
                      return {"code": 200, "message": " Check in successfully"}
                  else:
                      Response.status = "400"
                      return {"code": 401, "message": " Check in failed"}
                
        else:

            return json.dumps({'status': 'fail', 'message': 'Invalid Username'})

    @http.route('/user_attendence_out', methods=['POST'], type='json', auth='public')
    def user_last_check_out(self, **kw):
        # _logger.info('user_login')
        # api user employee attendence
        params = json.loads(request.httprequest.data);
        username =  params['username']
        check_out =  params['check_out']
        location_lat =  params['location_lat']
        location_long =  params['location_long']
        geolocation = location_lat + ',' + location_long
        user = request.env['res.users'].sudo().search([('login', '=', username)])

        if user:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
            if check_out:
                old_attendence = request.env['hr.attendance'].sudo().search(
                    [('employee_id', '=', employee.id), ('check_out', '=', False)])
                wrongtime = request.env['hr.attendance'].sudo().search([('check_in', '>', check_out), ('employee_id', '=', employee.id), ('check_out', '!=', False)])
                if wrongtime:
                    Response.status = "400"
                    return {"code": 401, "message": " You have already checked out at this time"}
                #"message": "\"Check Out\" time cannot be earlier than \"Check In\" time.",
                if not old_attendence:
                    Response.status = "400"
                    return {"code": 401, "message": " No check in record found"}
            
          #  else: 
            old_attendence.write({
                        'check_out': check_out,
                        'geo_check_out': geolocation
                    })
            Response.status = "200"
            return {"code": 200, "message": " Check out successfully"}
            if not old_attendence.check_in:
                   Response.status = "400"
                   return {"code": 401, "message": " No check in record found"}


    @http.route('/user_all_hreq', methods=['POST'], type='json', auth='public')
    def user_all_hreq(self, **kw):
        # _logger.info('user_login')
        # api user employee attendence
        params = json.loads(request.httprequest.data);
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
                    result['status'] = rec.state
                    list_of_result.append(result)
                return {
                    "success": {
                        "msg": "Holiday request successfully",
                        "data": list_of_result
                    }
                }
            else:
                Response.status = "400"
                return {"code": 401, "message": "no holiday request found"}
        else:

            return json.dumps({'status': 'fail', 'message': 'Invalid Username'})






    @http.route('/user_all_event', methods=['POST'], type='json', auth='public')
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
                   Response.status = "400"
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
                   Response.status = "400"
                   return {"code": 401, "message": "no event found"}
            else:

                return json.dumps({'status': 'fail', 'message': 'Invalid Username'})

    @http.route('/user_holiday_request', methods=['POST'], type='json', auth='public')
    def user_holiday_request(self, **kw):
        # _logger.info('user_login')
        # api user employee attendence
        params = json.loads(request.httprequest.data);
        username =  params['username']
        start_date = params['start_date']
        end_date = params['end_date']
        reason = params['reason']

        user = request.env['res.users'].sudo().search([('login', '=', username)])
        if user:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', username)])
            if start_date and end_date and reason:
                holiday = request.env['hr.leave'].sudo().create({
                    'employee_id': employee.id,
                    'request_date_from': start_date,
                    'request_date_to': end_date,
                    'holiday_status_id': 1,
                    'name': reason
                })

                Response.status = "200"
                return {"code": 200, "message": " Holiday request successfully"}
        else:

            return json.dumps({'status': 'fail', 'message': 'Invalid Username'})

    @http.route('/user_last_check', methods=['POST'], type='json', auth='public')
    def user_last_check(self, **kw):
        
        # api user employee attendence
        # params = request.get_json()
        params = json.loads(request.httprequest.data);
        username =  params['username']

        user = request.env['res.users'].sudo().search([('login', '=', username)])
        logging.info(user)
        if user:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
            attendence = request.env['hr.attendance'].sudo().search(
                [('employee_id', '=', employee.id)], order='id desc', limit=1)
            if attendence:
                return {"code": 200, "message": "Last check", "data": attendence.check_in, "check_out": attendence.check_out or ''}
               
            else:
                Response.status = "400"
                return {"code": 401, "message": " No check in record found"}
        else:

            return json.dumps({'status': 'fail', 'message': 'Invalid Username'})




    @http.route('/user_all_checks', methods=['POST'], type='json', auth='public')
    def user_all_check(self, **kw):
        
        # api user employee attendence
        # params = request.get_json()
        params = json.loads(request.httprequest.data);
        username =  params['username']

        user = request.env['res.users'].sudo().search([('login', '=', username)])
        logging.info(user)
        if user:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
            attendence = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee.id)])
            list_of_result = []
            if attendence:
                list_of_result = []
                for rec in attendence:
                    result = {}
                    result['check_in'] = rec.check_in
                    result['check_out'] = rec.check_out or ''
                    list_of_result.append(result)
                    return {"code": 200, "message": "Available Attendences", "data": list_of_result}
               
            else:
                Response.status = "400"
                return {"code": 401, "message": " No check in record found"}
        else:

            return json.dumps({'status': 'fail', 'message': 'Invalid Username'})
    

    @http.route('/user_employee_data', methods=['POST'], type='json', auth='public')
    def user_employee_data(self, **kw):
        
        # api user employee attendence
        # params = request.get_json()
        params = json.loads(request.httprequest.data);
        username =  params['username']

        user = request.env['res.users'].sudo().search([('login', '=', username)])
        logging.info(user)
        if user:
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
           
            if employee:
                return {
                    "success": {
                        "msg": "Employee data",
                        "data": {
                            "name": employee.name,
                            "work_email": employee.work_email,
                            "work_phone": employee.work_phone,
                            "work_mobile": employee.mobile_phone,
                            "work_location": employee.work_location_id.name,
                            "work_cordinate": employee.work_location_id.location_number,
                            "department_id": employee.department_id.name,
                            "job_id": employee.job_id.name,
                            "parent_id": employee.parent_id.name,
                            "pin": employee.pin,
                            "resource_calendar_id": employee.resource_calendar_id.name

                        }
                    }
                }
            else:
                Response.status = "400"
                return {"code": 401, "message": " No employee found"}
        else:

            return json.dumps({'status': 'fail', 'message': 'Invalid Username'})

    @http.route('/user_login', methods=['POST'], type='json', auth='public', csrf=False)
    def user_login(self, **kw):
        request_body = {}
        if kw:
            request_body = kw.copy()
        elif request.httprequest.data:
            request_body = json.loads(request.httprequest.data)
        else:
            Response.status = "403"
            return {"code": 403, "status": "Forbidden!", "message": "Messing data!"}
            
        # login_validator = ValidatorFactory(request_body, "login")
        # if not login_validator.isvalid():
        #     invalid_data = login_validator.get_unprocessable_entities()
        #     Response.status = "422"
        #     return {"code": 422, "status": "Unprocessable Entity", "message": invalid_data}
            
        def create_response(code, message, data=None):
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "result": {
                    "code": code,
                    "message": message
                }
            }
            if data:
                response["result"]["data"] = data
            return json.dumps(response)

        try:
            user_env = request.env['res.users']
            user = user_env.with_user(SUPERUSER_ID).search([('login', '=', request_body.get('username'))])

            # Check if user exists
            if not user:
               Response.status = "400"
               return {"code": 401, "message": " Username or Password is incorrect"}
            user_env.with_user(user)._check_credentials(password=request_body.get('password'),
                    user_agent_env={'interactive': False})
            # user.generate_access_token()
            # return create_response(200, "User Logged In successfully", {
            # "id": user.id,
            # "name": user.partner_id.name,
            # "username": user.login,
            # "location_long": user.employee_id.work_location_id.x_studio_long,
            # "location_lat": user.employee_id.work_location_id.x_studio_lat,
            # })
            Response.status = "200"
            return {
                "id": user.id,
                "name": user.partner_id.name,
                "username": user.login,
                "Employee_postition": user.employee_id.job_id.name or '',
                "employee_birthdate": user.employee_id.birthday  or '',
                "employee_email": user.employee_id.work_email or '',
                "start_date": user.employee_id.start_date or '',
                "location_long": user.employee_id.work_location_id.longitude or '',
                "location_lat": user.employee_id.work_location_id.latitude or '',
            }
        except AccessDenied as e:
            if "password" in str(e):
               Response.status = "400"
               return {"code": 401, "message": " Username or Password is incorrect"}
            else:
                  Response.status = "400"
                  return {"code": 401, "message": " Username or Password is incorrect"}

        # except AccessDenied as e:
        #     if "password" in str(e):
        #         return {"code": 401, "message": "Incorrect username or password"}
        #     else:
        #        return {"code": 401, "message": "Incorrect username or password"}


        # try:
        #     user_env = request.env['res.users']
        #     user = user_env.with_user(SUPERUSER_ID).search([('login', '=', request_body.get('username'))])
        #     user_env.with_user(user)._check_credentials(password=request_body.get('password'),
        #                                                 user_agent_env={'interactive': False})
        #     # user.generate_access_token()
        # except AccessDenied:
        #     Response.status = "400"
        #     return {"code": 401, "message": " Username or Password is incorrect"}
        # Response.status = "200"
        # return {"code": 200, "message": "User Logged In successfully",
        #         "data": {"id": user.id, "name": user.partner_id.name, "username": user.login, "loaction_long": user.employee_id.work_location_id.x_studio_long, "location_lat": user.employee_id.work_location_id.x_studio_lat,}}

    @http.route('/user_activities', methods=['POST'], type='json', auth='public')
    def user_activities(self, **kw):
        params = json.loads(request.httprequest.data);
        username =  params['username']

        user = request.env['res.users'].sudo().search([('login', '=', username)])
        if user:
            activities = request.env['mail.activity'].sudo().search([('user_id', '=', user.id)])
            if activities:
                list_of_result = []
                for rec in activities:
                    result = {}
                    result['date_deadline'] = rec.date_deadline
                    result['activity_id'] = rec.id
                    result['summary'] = rec.summary
                    result['activity_category'] = rec.activity_category
                    result['note'] = rec.note
                    result['res_id'] = rec.res_id
                    result['model'] = rec.x_studio_model
                    result['state'] = rec.state
                    result['res_name'] = rec.res_name
                    result['activity_type_id'] = rec.activity_type_id.name
                    result['user_id'] = rec.user_id.name
                    list_of_result.append(result)
                return {
                    "success": {
                        "msg": "Available activities",
                        "data": list_of_result
                    }
                }
            else:
                Response.status = "400"
                return {"code": 401, "message": " No activities found"}
        else:
                
                return json.dumps({'status': 'fail', 'message': 'Invalid Username'})
    @http.route('/holiday_types', methods=['GET'], type='json', auth='public')
    def holiday_types(self, **kw):
        holiday_types = request.env['hr.leave.type'].sudo().search([])
        list_of_result = []
        for rec in holiday_types:
            result = {}
            result['name'] = rec.name
            result['id'] = rec.id
        
            list_of_result.append(result)
        return {
            "success": {
                "msg": "Available holiday types",
                "data": list_of_result
            }
        }

    @http.route('/update_activity', methods=['POST'], type='json', auth='public')
    def update_activity(self, **kw):
        params = json.loads(request.httprequest.data);
        username =  params['username']
        activity_id =  params['activity_id']
        note =  params['note']
        done =  params['done']
        user = request.env['res.users'].sudo().search([('login', '=', username)])
        if user:
            activity = request.env['mail.activity'].sudo().search([('id', '=', activity_id)])
            if activity:
                activity.write({'note': note})
                if done == 'true':
                    activity.action_done()
                activity.action_done()
                return {
                    "success": {
                        "msg": "Activity updated successfully"
                    }
                }
          
                
            else:
               Response.status = "400"
               return {"code": 401, "message": " No activities found"}
            
        else:
                
                return json.dumps({'status': 'fail', 'message': 'Invalid Username'})