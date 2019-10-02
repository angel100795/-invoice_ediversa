# -*- coding: utf-8 -*-


from openerp import _, api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import base64
from datetime import datetime
# TRABAJAR CON LOS EXCEL
import xlsxwriter
import time

import tempfile

# SOLUCIONA CUALQUIER ERROR DE ENCODING (CARACTERES ESPECIALES)
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

class export_factura_txt(models.Model):
    _name = 'export.factura.txt'
    _description = 'Exportar Factura'
    datas_fname = fields.Char('File Name', size=256)
    dtm_creacion = fields.Datetime ('Fecha creacion', readonly = False, select = True 
                                , default = lambda self: fields.datetime.now ())
    inv_numdoc = fields.Char('Numero de factura', size=256)
    inv_tipo = fields.Selection([
        ('380', 'Factura comercial'),
        ('381', 'Nota de adono'),
        ('325', 'Factura pro-forma'),
        ('383', 'Nota de cargo'),
        ('384', 'Factura Corregida'),
        ('385', 'Factura recapitulada'),
        ('389', 'Autofactura')],
        'Tipo de documento')
    inv_funcion = fields.Selection([
        ('9', 'Original'),
        ('5', 'Sustitucion'),
        ('7', 'Duplicado'),
        ('43', 'Transmisión adcional'),
        ('31', 'Copia'),
        ('2', 'Adición (Complementaria)')],
        'Función del mensaje')

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

    pat_cali = fields.Selection([
        ('1', 'Básico'),
        ('21', 'Varios vencimientos'),
        ('35', 'Pago único')],
        'Condiciones de pago')
    pat_ven = fields.Datetime ('Fecha de vencimiento', readonly = False, select = True 
                                , default = lambda self: fields.datetime.now ())
    pat_import = fields.Float('Importe del vencimiento')
    pat_efect = fields.Datetime ('Fecha de efectiva', readonly = False, select = True 
                                , default = lambda self: fields.datetime.now ())
    pat_referencia = fields.Selection([
        ('5', 'Después de la fecha factura'),
        ('72', 'Fecha de pago'),
        ('29', 'Depués de la fecha de entrega'),
        ('68', 'Fecha de valor')],
        'Referencia de tiempo de pago')
    pat_periodo = fields.Selection([
        ('D', 'Días'),
        ('M', 'Meses')],
        'Tipo de periodo')
    pat_numero = fields.Integer('Numero de días o meses')
    pat_entrega = fields.Datetime ('Fecha de entrega', readonly = False, select = True 
                                , default = lambda self: fields.datetime.now ())
    moares_neto = fields.Integer('Importe neto de la factura')
    moares_bruto = fields.Integer('Importe bruto')
    moares_base = fields.Integer('Base imponible')
    moares_total = fields.Integer('Importe total de la factura')
    moares_impuestos = fields.Integer('Total de impuestos')
    moares_descuentos = fields.Integer('Total de descuentos globales')
    moares_cargos = fields.Integer('Total de cargos globales')
    moares_debido = fields.Integer('Importe total a pagar')

    taxres_tipo = fields.Selection([
        ('VAT', 'IVA'),
        ('IGI', 'IGIC'),
        ('EXT', 'Exento de impuesto'),
        ('ACT', 'Impuesto de alcoholes'),
        ('RE', 'Recargo de equivalencia'),
        ('ENV', 'Punto verde')],
        'Calificador de tipo de impuesto')
    taxres_porcentaje = fields.Integer('Porcentaje del impuesto aplicar')
    taxres_importe = fields.Integer('Suma total de los importes del impuesto')
    taxres_base = fields.Integer('Importe monetario de la base imponible') 
    taxres_total = fields.Integer('Importe del impuesto')
    taxres_dis = fields.Integer('Disposición nacional que da lugar a la exención del IVA')
    taxres_categoria = fields.Selection([
        ('E', 'Exento de impuestos'),
        ('ES1', 'Se aplica el régimen especial del criterio de caja')],
        'Categoría del impuesto')

    
    file = fields.Binary('Layout')
    download_file = fields.Boolean('Descargar Archivo')
    cadena_decoding = fields.Text('Binario sin encoding')
    type = fields.Selection([('txt', 'TXT')], 'Tipo Exportacion',
                            required=False, )

    _defaults = {
        'download_file': False,
        'type': 'txt',
    }

    @api.multi
    def export_txt_file(self):
        document_txt = ""

        #split de fecha creacion
        split_creacion = self.dtm_creacion.split('-')
        split_creacion_dia = split_creacion[2].split(' ')
        date_creacion = split_creacion[0]+split_creacion[1]+split_creacion_dia[0]
        
        sl = "\n"
        # =>Cabecera
        campo_inv = "%s|%s|%s|%s" % (
                "INV", self.inv_numdoc, self.inv_tipo, self.inv_funcion)
        campo_dtm = "%s|%s" % (
                "DTM", date_creacion)
        campo_pai = "%s|%s" % (
                "PAI", self.pai)  
        # =>Fin Cabecera

        #creamos el archivo txt
        file_name = 'desdav.txt'
        date = datetime.now().strftime('%d-%m-%Y')
        datas_fname = "Factura "+str(date)+".txt"  # Nombre del Archivo
        

        #abrimos el archivo txt especificando en que ruta de la maquina se guardara
        document_txt = document_txt+"INVOIC_D_93A_UN_EAN007" + sl + campo_inv + sl + campo_dtm +sl + campo_pai
        with open('/tmp/'+file_name, 'w+') as f:
            #le asiganamos que informacion guardara
            f.write(document_txt)
        f.close()
        with open('/tmp/'+file_name, 'r+') as r:
            print "rrrrrrrrrrr", r
            self.write({
                        'cadena_decoding': document_txt,
                        'datas_fname': datas_fname,
                        'file': base64.b64encode(r.read()),
                        'download_file': True})
            print "f.read()", r.read()
        r.close()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.factura.txt',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }




