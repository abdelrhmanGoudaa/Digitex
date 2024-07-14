from odoo import http
from odoo.http import request
import json
from odoo.http import Response
from urllib.parse import parse_qs

class EmployeeApi(http.Controller):
    '''Creating Apis for employees CRUD operations
        get all employees
        add employee --
    '''
    @http.route(route="/api/employee",methods=["GET","POST"],csrf=False,auth="none",type="http")
    def get_employees(self):
        print(self,"This is employee get test")
        if request.httprequest.method == "GET" :
            employees_obj = request.env['hr.employee'].sudo().search([])
            vals = []
            for emp in  employees_obj:
                val = {
                    "name":emp.name,
                    "id": emp.id,
                    "address_home_id": emp.address_home_id.id,
                    "resource_calendar_id": emp.resource_calendar_id.id
                }
                vals.append(val)
            response = json.dumps(vals)
            return http.Response(response,status=200, mimetype='application/json')
        elif request.httprequest.method == "POST":
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            print(vals)
            request.env['hr.employee'].sudo().create(vals)


    @http.route(route='/api/addemp',methods=["POST"],csrf=False,auth="none",type="json")
    def post_request(self):
        
        mactivty = request.env['mail.activity'].sudo().search([],limit=1)
        print(mactivty)
        print(mactivty.id)
        print(request.jsonrequest)
        vals = request.jsonrequest
        print('helllo post request ')
        print(request.httprequest)
        print(request.httprequest.data.decode())
        if vals:
            request.env['todo.line'].sudo().create(vals)
        else:
            return {"message":"No Data sent"}


    @http.route(route="/api/updatemp/<int:id>", type='json', methods=['PUT'], auth="none", csrf=False)
    def update_put(self, id):
        print(id)
        obj = request.env['todo.line'].sudo().search([('id', '=', id)])
        print(obj)

        if not obj:
            data = json.dumps({"message": "PLEASE!!, give a valid id", "status": 400})
            headers = [('Content-Type', 'application/json')]
            return {"message": "ERRRRRRRRRRRRRRRRRORRRRRRRRRR"}

        # Get the data from request body
        vals = request.jsonrequest
        print(vals)
        obj.write(vals)

        # return request.make_response(
        #     json.dumps({"message": "Record updated successfully", "status": 200}),
        #     headers=[('Content-Type', 'application/json')]
        # )

    @http.route(route="/api/getitem/<int:id>", type='http', methods=['GET'], auth="none", csrf=False)
    def get_item(self,id):
        print(id)
        object = request.env['todo.line'].sudo().search([('id','=',id)])
        print(object)
        if not object:
            res = {'message' : 'Please provide a valid id'}
            return request.make_response(data=json.dumps(res))
        
        
        try:

            res = {
                "name": object.name,
                "id": object.id
            }
            return request.make_response(data=json.dumps(res))
        except Exception as e:
            return Response(f'error {e}',status='500')


    @http.route(route='/api/delitem/<int:id>',type='http',methods=['DELETE'],auth="none",csrf=False)
    def del_item(self,id):
        # search on the id inside db table
        obj = request.env['todo.line'].sudo().search([('id','=',id)])

        # check if the id exists
        if not obj:
            res = {'error' : 'Please provide a valid id to delete'}
            Response(status='404')
            return request.make_response(data=json.dumps(res))
       
        try:
            obj.unlink()
            res = {"message":"record has been deleted success fully"}
            return request.make_response(data=json.dumps(res))
        except Exception as e:
            return Response(f'error {e}',status='500')

    @http.route(route='/api/getitems',type='http',methods=['GET'],auth='none',csrf=False)
    def get_items(self):
    
        # get the params
        params = request.httprequest.query_string.decode('utf-8')
        print(params)
        params = parse_qs(request.httprequest.query_string.decode('utf-8'))
        print(params)

        # check if there any params
        query_param = []

        if params:
            param_val = params.get('is_done')[0].lower()
            if param_val == 'false' :
                param_val = False
            query_param.append(('is_done','=',param_val))
            print(query_param)
        
        objs = request.env['todo.line'].sudo().search(query_param)

        if not objs:
            res = {'error' : 'Please give a vlid parameters'}
            Response(status='404')
            return request.make_response(data=json.dumps(res))
        
        # return the data depend on the params
        try:
            vals = []
            for obj in objs:
                # print(obj.is_done)
                val = {
                    "name": obj.name,
                    "active": obj.is_done
                }
                vals.append(val)
            return request.make_response(data=json.dumps(vals))
        except Exception as e:
            return Response(f'error {e}',status='500')
        
    
    @http.route(route='/testing',type='http',auth='user',methods=['GET'],csrf=False)
    def test_endpoint(self):
        user = request.env.user
        print(user)
        print('Test endpoint @'* 4)
        print('#'* 4)
        return '[request.make_response(data={"Testing Method"})]'




'''

    @http.route('/your/route', type='json', auth='public', methods=['POST'], csrf=False)
    def your_method(self, **post):
        # Your logic to check vendor
        if not vendor:
            # Create JSON response with status code 401
            response = Response(json.dumps({'message': 'Invalid vendor'}), status=401, content_type='application/json')
            return response
'''