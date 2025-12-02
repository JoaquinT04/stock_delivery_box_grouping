# -*- coding: utf-8 -*-
{
    'name': "Agrupación por Cajas en Entrega (Adhoc Compatible)",
    'summary': "Agrupa líneas de remito por número de caja (Estilo Reporte Cliente).",
    'description': """
        Requerimiento Personalizado:
        1. Mapea campo 'x_studio_caja' en stock.move y stock.move.line.
        2. Modifica el Reporte de Remito (Delivery Slip) para agrupar por cajas.
        3. Lógica inteligente: Si no hay caja en el detalle, toma la del movimiento padre.
        
        Compatible con: Odoo 18 Enterprise, l10n_ar_stock y stock_ux.
    """,
    'author': "Tu Empresa / Desarrollador Odoo",
    'website': "https://tusitio.com",
    'category': 'Inventory/Delivery',
    'version': '18.0.1.0.2',
    'license': 'OPL-1',
    'depends': [
        'stock', 
        'stock_delivery', 
        'l10n_ar_stock',  # Dependencia clave para heredar sobre la localización
        'stock_ux'        # Dependencia clave de Adhoc
    ],
    'data': [
        'views/stock_move_line_views.xml',
        'reports/stock_report_delivery.xml',
    ],
    'installable': True,
    'application': False,
}