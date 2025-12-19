# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[
        ('vehicle_roll', 'Etiqueta Vehículo (Rollo)')
    ], ondelete={'vehicle_roll': 'set default'})


    def _prepare_report_data(self):
        if self.print_format == 'vehicle_roll':
            
            xml_id = 'stock_delivery_box_grouping_module.report_product_vehicle_label'
            
            moves = self.move_ids
            if not moves and self._context.get('active_model') == 'stock.picking':
                picking_ids = self._context.get('active_ids') or [self._context.get('active_id')]
                moves = self.env['stock.move'].search([('picking_id', 'in', picking_ids)])

            # DEVOLVEMOS LISTA DE IDs (Enteros)
            return xml_id, {
                'move_ids_list': moves.ids,  # Pasamos solo IDs
                'active_model': 'stock.move'
            }
        
        return super()._prepare_report_data()