# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[
        ('vehicle_roll', 'Etiqueta Vehículo (Rollo)')
    ], ondelete={'vehicle_roll': 'set default'})


    def _prepare_report_data(self):
        if self.print_format == 'vehicle_roll':
            # Llamamos al super para obtener la data base
            xml_id, data = super()._prepare_report_data()
            
            # --- CORRECCIÓN DE CANTIDAD ---
            # Si quieres forzar que siempre salga 1 etiqueta por producto
            # independientemente de la cantidad del remito:
            new_quantities = {}
            for product_id, qty in data.get('quantity_by_product', {}).items():
                # Forzamos 1 unidad por producto
                new_quantities[product_id] = 1 
            
            data['quantity_by_product'] = new_quantities
            # ------------------------------

            # XML ID correcto
            xml_id = 'stock_delivery_box_grouping_module.report_product_vehicle_label'
            return xml_id, data
        
        return super()._prepare_report_data()