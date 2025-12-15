# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductVehicleBrand(models.Model):
    _name = 'product.vehicle.brand'
    _description = 'Marca de Vehículo'
    _order = 'name'

    name = fields.Char(string="Marca", required=True, index=True)
    # Guardamos la imagen aquí. Una sola vez por Marca.
    logo = fields.Image(string="Logo", max_width=512, max_height=512)
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', '¡El nombre de la marca debe ser único!')
    ]