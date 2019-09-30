# -*- coding: utf-8 -*-


from openerp import _, api, fields, models

from openerp.tools.translate import _
from openerp.exceptions import except_orm, Warning, RedirectWarning




class export_factura_txt(models.Model):
    _name = 'export.factura.txt'
    _description = 'Exportar Albaran'