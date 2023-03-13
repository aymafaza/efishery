from odoo import http
from odoo.http import request
import jwt

class Authentication(http.Controller):
    @http.route('/auth/login', type='json', auth="public", methods=['POST'], csrf=False)
    def authenticate(self, **params):
        db = params.get("db")
        username = params.get("username")
        password = params.get("password")
        uid = request.session.authenticate(db or request.session.db, username, password)
        # if uid:
        #     encoded_jwt = jwt.encode({"some": "payload"}, "PLACE_SECRET_HERE_SOON", algorithm="HS256")
        # return request.env['ir.http'].session_info()
        if uid:
            email = request.env['ir.http'].session_info().get('username')
            role = request.env['ir.http'].session_info().get('is_admin')
            encoded_jwt = jwt.encode({"email": email, "is_admin": role}, "PLACE_SECRET_HERE_SOON", algorithm="HS256")
            return encoded_jwt
        