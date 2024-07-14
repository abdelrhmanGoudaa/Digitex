from odoo import http
from odoo.http import request
from datetime import datetime
import json

class TestApi(http.Controller):

    @http.route(route="/api/test",methods=["GET"],csrf=False,auth="none",type="http")
    def test_api(self):
        print(request.auth_method)
        print(request)
        print(request.uid)



    @http.route('/template', type='http', auth='none', methods=['GET'], csrf=False)
    def custom_template(self, **kwargs):
        print('Route: custom_template')
        # Get the current user's id
        user_id = request.session.uid
        print(user_id)
        # Search for the hr.employee record related to the current user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)], limit=1)
        if employee:
            employee_id = employee.id
            # name = employee.name if employee else "Unknown"
            print(f'Employee ID: {employee_id}')
            # Get the current date
            current_date = datetime.now().date()
            print(current_date)
            # Search for the hr.attendance records related to the employee_id and create_date before the current date
            # Search for the hr.attendance records related to the employee_id and create_date equals to the current date
            employee_attendance = request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee_id),
                ('create_date', '>=', datetime.combine(current_date, datetime.min.time())),
                ('create_date', '<', datetime.combine(current_date, datetime.max.time()))
            ],limit=1)

            childs_attendance = request.env['hr.attendance'].sudo().search([
                ('employee_id', 'in', employee.child_ids.ids),
                ('create_date', '>=', datetime.combine(current_date, datetime.min.time())),
                ('create_date', '<', datetime.combine(current_date, datetime.max.time()))
            ])
            if employee_attendance:
                print(employee_attendance)
                print(childs_attendance.ids)
                # Update the latitude and longitude fields
                # latitude = "30.0444"
                # longitude = "31.2357"
                # for rec in employee_attendance:
                    # rec.sudo().write({
                    #     'lat_longin': latitude,
                    #     'long_longin': longitude
                    # })
                    # latitude = rec.lat_longin if employee else 0.0
                    # longitude = rec.long_longin if employee else 0.0
                    # print('lat',latitude)
                    # print('long',longitude)
                return request.render(template='hr_apis.test_template_view',
                    qcontext={'employee': employee_attendance, 'child_emps': childs_attendance})
                return request.render(template='hr_apis.test_template_view',
                    qcontext={'name': name, 'latitude': latitude, 'longitude': longitude, 'child_emps': childs_attendance})
            else:
                return "<h1>No Current Checkins For Today</h1>"

            # latitude = "30.0743"
            # longitude = "31.242"
            # for rec in childs_attendance:
            #     # rec.sudo().write({
            #     #     'lat_longin': latitude,
            #     #     'long_longin': longitude
            #     # })
            #     latitude = rec.lat_longin if employee else 0.0
            #     longitude = rec.long_longin if employee else 0.0
        else:
            return json.dumps({
                "error" : "Please Provide a right employee"
            })
        # child_emps = []
        # print(employee.child_ids.ids)
        # for child in employee.child_ids:
        #     child_emps.append(child)
        # print(child_emps)
        # Extract name, latitude, and longitude from the employee record
        # name = employee.name if employee else "Unknown"
        # latitude = employee.lat if employee else 0.0
        # longitude = employee.long if employee else 0.0

'''
SELECT create_date,long_longin,lat_longin FROM hr_attendance WHERE employee_id = 7  AND create_date::date = '2024-06-30';

'''