# -*- coding: utf-8 -*-
from openerp import http

# class Dhuicrm(http.Controller):
#     @http.route('/dhuicrm/dhuicrm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dhuicrm/dhuicrm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dhuicrm.listing', {
#             'root': '/dhuicrm/dhuicrm',
#             'objects': http.request.env['dhuicrm.dhuicrm'].search([]),
#         })

#     @http.route('/dhuicrm/dhuicrm/objects/<model("dhuicrm.dhuicrm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dhuicrm.object', {
#             'object': obj
#         })