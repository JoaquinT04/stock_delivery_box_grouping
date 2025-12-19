# -*- coding: utf-8 -*-
from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    box_number = fields.Integer(
        string='Nro. Caja',
        copy=True,
        help="Número de caja asignado a esta linea"
    )