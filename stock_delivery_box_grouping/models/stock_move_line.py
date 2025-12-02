# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # Definimos el campo con el nombre técnico que usaba Studio.
    x_studio_caja = fields.Char(
        string='Nro. Caja',
        index=True,
        copy=False,
        help="Identificador manual de la caja (Migrado de Studio a Código)."
    )

