# -*- coding: utf-8 -*-
from odoo import models, fields

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    box_number = fields.Integer(
        string='Nro. Caja',
        # La magia: hereda del padre (move_id), se guarda en BD, pero es editable.
        related='move_id.box_number',
        store=True,
        readonly=False,
        group_operator='max', # Para que no sume los números de caja en las vistas pivot
        help="Hereda del movimiento, pero puede ser modificado específicamente para esta línea."
    )