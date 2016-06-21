# -*- coding: utf-8 -*-
from openerp import http

# class Dhuitask(http.Controller):
#     @http.route('/dhuitask/dhuitask/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dhuitask/dhuitask/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dhuitask.listing', {
#             'root': '/dhuitask/dhuitask',
#             'objects': http.request.env['dhuitask.dhuitask'].search([]),
#         })

#     @http.route('/dhuitask/dhuitask/objects/<model("dhuitask.dhuitask"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dhuitask.object', {
#             'object': obj
#         })