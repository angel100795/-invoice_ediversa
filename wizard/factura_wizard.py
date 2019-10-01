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
        'Referencias', required=True)
    rff_referencia = fields.Char('Referencia del documento')
    rff_fecha = fields.Char('Fecha de referecia')
    nadsco = fields.Char('codigo EDI emisor')
    nadbco = fields.Char('codigo EDI receptor')
    nadsu_cod_prove = fields.Char('codigo EDI Proveedor')
    nadby_cod_cliente = fields.Char('codigo EDI Cliente')
    nadiv = fields.Char('Codigo EDI a quien se factura')
    nadms = fields.Char('Codigo EDI del emisor del mensaje')
    nadmr = fields.Char('Codigo EDI del receptor del mensaje')
    naddp = fields.Char('Codigo EDI del receptor de la mercancía')
    nadpr = fields.Char('Codigo EDI del emisor del pago')
    nadpe = fields.Char('Codigo EDI del receptor que paga')
    cux_coin = fields.Selection([
        ('EUR', 'Euro'),
        ('USD', 'Dolar')],
        'Codigo de moneda', required=True)
    cux_cali = fields.Selection([
        ('4', 'Divisa de la factura'),
        ('10', 'Divisa del precio'),
        ('11', 'Divisa del pago')],
        'Codigo de moneda', required=True)
