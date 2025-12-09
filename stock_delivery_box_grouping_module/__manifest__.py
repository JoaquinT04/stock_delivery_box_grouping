# -*- coding: utf-8 -*-
{
    'name': "Agrupación por Cajas en Entrega (Adhoc Compatible)",
    'summary': "Remitos agrupados y Etiquetas de Despacho por Caja.",
    'description': """
        Requerimiento Personalizado:
        1. Agrupación en Remitos.
        2. Etiquetas de Despacho por Caja.
    """,
    'author': "Tu Nombre / Empresa",
    'website': "https://tusitio.com",
    'category': 'Inventory/Delivery',
    'version': '18.0.1.0.3',
    'license': 'OPL-1',
    'depends': [
        'stock', 
        'stock_delivery', 
        'l10n_ar_stock', 
        'stock_ux'
    ],
    'data': [
        'reports/paper_formats.xml',       
        'reports/stock_report_delivery.xml',
        'reports/stock_label_dispatch.xml', 
    ],
    'installable': True,
    'application': False,
}