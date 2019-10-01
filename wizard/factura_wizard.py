# -*- coding: utf-8 -*-


from openerp import _, api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

class export_factura_txt(models.Model):
    _name = 'export.factura.txt'
    _description = 'Exportar Factura'


    type = fields.Selection([('txt', 'TXT')], 'Tipo Exportacion',
                            required=False, )
    dtm_creacion = fields.Datetime ('Fecha creacion', readonly = False, select = True 
                                , default = lambda self: fields.datetime.now ())
    pai = fields.Selection([
        ('20', 'Cheque'),
        ('42', 'A una cuenta bancaria'),
        ('60', 'Pagaré'),
        ('14E', 'Giro de banco'),
        ('10', 'En efectivo')],
        'Instruccion de pago')

    ali = fields.Selection([
        ('1A', 'Devolución de la mercancía'),
        ('2A', 'Bonificacion por volumen'),
        ('3A', 'Diferencias (precio,cantidad,etc.)'),
        ('78E', 'Devolucion de la mercancia'),
        ('79E', 'Discrepancias o ajustes'),
        ('80E', 'Bonificaciones anuales (Rappel)')],
        'Condiciones especiales')
    
    rff_cali = fields.Selection([
        ('DQ', 'Numero de albaran en papel'),
        ('ON', 'Numero de pedido'),
        ('AAN', 'Numero de planificacion de entregas')],
        'Referencias', required=True, default="ON")
    rff_referencia = fields.Char('Referencia del documento')
    rff_fecha = fields.Char('Fecha de referecia')