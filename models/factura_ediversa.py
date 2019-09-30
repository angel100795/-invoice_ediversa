# -*- coding: utf-8 -*-


from openerp import _, api, fields, models
from openerp.exceptions import Warning
import logging
from pprint import pprint

class ediversaOrder(models.Model):
    _name = 'ediversa.order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'ediversa Orders'

    _rec_name = 'subject'

    subject = fields.Char('Subject', size=128)
    email = fields.Char('Email', size=128)
    attach = fields.Text('Attachment')
