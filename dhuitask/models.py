# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class dhuitask(osv.osv):
    _inherit = 'project.task'

    _columns = {}

class dhuitask_type(osv.osv):
    _name = 'dhuitask.type'
    _inherit = 'project.task.type'

    _columns = {}