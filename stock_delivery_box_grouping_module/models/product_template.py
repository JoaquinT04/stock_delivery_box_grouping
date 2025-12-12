# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Relación Many2one: Ligero, eficiente.
    vehicle_brand_id = fields.Many2one(
        'product.vehicle.brand',
        string="Marca del Vehículo",
        help="Seleccione la marca para que salga el logo en la etiqueta."
    )
    
    # El modelo específico (Fox, Gol, Hilux)
    vehicle_model_text = fields.Char(
        string="Modelo Compatible",
        help="Ej: Fox / Suran / Gol Trend"
    )