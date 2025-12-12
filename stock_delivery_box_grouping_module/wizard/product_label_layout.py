# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[
        ('vehicle_roll', 'Etiqueta Vehículo (Rollo)')
    ], ondelete={'vehicle_roll': 'set default'})

    def _prepare_report_data(self):
        if self.print_format == 'vehicle_roll':
            xml_id, data = super()._prepare_report_data()
            
            # IMPORTANTE: Reemplaza 'stock_delivery_box_grouping_module' 
            # por el nombre REAL de tu carpeta en Odoo.sh si es diferente.
            xml_id = 'stock_delivery_box_grouping_module.report_product_vehicle_label'
            
            return xml_id, data
        
        return super()._prepare_report_data()