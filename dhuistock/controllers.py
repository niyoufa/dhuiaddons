# -*- coding: utf-8 -*-
from openerp import http

# class Dhuistock(http.Controller):
#     @http.route('/dhuistock/dhuistock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dhuistock/dhuistock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dhuistock.listing', {
#             'root': '/dhuistock/dhuistock',
#             'objects': http.request.env['dhuistock.dhuistock'].search([]),
#         })

#     @http.route('/dhuistock/dhuistock/objects/<model("dhuistock.dhuistock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dhuistock.object', {
#             'object': obj
#         })