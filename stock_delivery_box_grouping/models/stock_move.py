# -*- coding: utf-8 -*-
from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    # Mapeamos el campo que ya tienes en la vista de Operaciones (creado orig. por Studio)
    # Esto permite que el reporte acceda a este dato si la linea detallada está vacía.
    x_studio_caja = fields.Char(
        string='Nro. Caja (Move)',
        copy=False,
        help="Caja asignada a nivel de movimiento general."
    )