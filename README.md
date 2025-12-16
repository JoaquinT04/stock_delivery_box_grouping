## 📋 Descripción General

Este módulo extiende las capacidades del módulo de Inventario para adaptar la documentación de salida a flujos logísticos que requieren agrupación por cajas y etiquetado específico de autopartes.

Incluye tres funcionalidades principales:
1.  **Remito por Cajas (Nuevo Reporte):** Un documento de entrega alternativo que agrupa ítems por número de caja, con diseño nativo y soporte para la localización argentina.
2.  **Etiquetas de Despacho:** Generación de etiquetas identificatorias para pegar en cada caja física.
3.  **Etiquetas de Producto (Vehículo):** Un sistema de etiquetado en rollo (100x50mm) que incluye logo de la marca del vehículo, códigos de barra grandes y datos técnicos.

---

## 🛠️ Implementación Técnica

### 1. Gestión de Cajas (Backend)
Se profesionalizó la gestión del número de caja, migrando de campos de texto (Studio) a una estructura de datos robusta:

*   **Campo `box_number` (Integer):** Se creó este campo en `stock.move` y `stock.move.line`. Al ser entero, permite un ordenamiento natural correcto (1, 2, 10...) en lugar de alfanumérico (1, 10, 2...).
*   **Sincronización Automática:** El campo en la línea detallada (`stock.move.line`) es `related` al movimiento padre (`stock.move`) pero **editable**. Esto significa que si el usuario asigna la "Caja 1" en la vista general, todas las líneas heredan ese dato, pero permite excepciones manuales en el detalle.
*   **Vistas:** Se inyectó la columna "Nro. Caja" tanto en la pestaña de Operaciones como en Operaciones Detalladas del Picking.

### 2. Reporte: Remito por Cajas (Punto 1 y 2)
Se desarrolló un reporte QWeb totalmente nuevo (`report_delivery_by_box`) independiente del estándar para evitar conflictos con módulos de terceros (Adhoc).

*   **Lógica de Agrupación:** El reporte itera sobre los números de caja únicos. Los productos sin caja asignada se agrupan al final bajo "Sin Agrupar".
*   **Diseño "Theme Aware":** El reporte detecta automáticamente los colores de la compañía (`primary_color`, `secondary_color`) y el diseño configurado en Odoo (Light, Boxed, Striped), adaptando bordes, títulos y tablas para que parezca un reporte nativo.
*   **Cabecera Híbrida:** Se diseñó una cabecera que respeta el logo y dirección de la empresa (estándar Odoo) pero integra la información fiscal de Argentina (Responsabilidad AFIP, CUIT, etc.) de forma limpia.
*   **Contenedor de Info:** Se creó un bloque de información que agrupa "Cliente" y "Datos del Pedido" en una estructura de columnas alineada, mejorando la legibilidad.

### 3. Etiquetas de Despacho (Punto 2)
*   **Reporte:** `stock_label_dispatch.xml`.
*   **Funcionalidad:** Genera una página por cada caja distinta presente en el remito.
*   **Diseño:** Muestra el número de caja en tamaño gigante y una tabla resumen con el contenido de esa caja específica.

### 4. Etiquetas de Producto / Vehículo (Punto 3)
Se implementó una solución completa para imprimir etiquetas en impresoras de rollo (Zebra/Datamax) de 100x50mm.

*   **Modelo de Marcas (`product.vehicle.brand`):** Para evitar la duplicidad de datos, se creó un modelo catálogo para las marcas (VW, Ford, etc.). La imagen del logo se guarda **una sola vez** en este modelo y los productos la referencian.
*   **Campos en Producto:**
    *   `vehicle_brand_id`: Relación con la marca.
    *   `vehicle_model_text`: Campo de texto para el modelo específico (ej. "Fox / Suran").
*   **Wizard Extendido:** Se heredó `product.label.layout` para agregar la opción **"Etiqueta Vehículo (Rollo)"** al menú de impresión estándar de Odoo.
*   **Lógica de Cantidades:** Se modificó el wizard para que utilice la **Demanda Inicial** (`product_uom_qty`) en lugar de la cantidad hecha. Esto permite imprimir etiquetas completas antes de realizar el picking.
*   **Motor de Renderizado (Hard Reset):** Para solucionar los problemas de márgenes de `wkhtmltopdf` que generaban páginas en blanco:
    *   Se inyectaron estilos CSS globales (`html, body { margin: 0 }`).
    *   Se definió una altura lógica de **44mm** (para papel de 50mm) y `overflow: hidden`.
    *   Se construyó el diseño con **Tablas HTML rígidas**, garantizando que el logo y el código de barras nunca se superpongan ni se corten.

---

## 🚀 Flujo de Uso

### A. Imprimir Remito Agrupado
1.  Vaya a un **Remito (Transferencia)**.
2.  Asegúrese de haber cargado los números en la columna **"Nro. Caja"**.
3.  Haga clic en el botón **Imprimir**.
4.  Seleccione **"Remito por Cajas (Nativo)"**.
5.  *Resultado:* Un PDF A4 con los productos agrupados visualmente por caja y totales parciales.

### B. Imprimir Etiquetas de Despacho (Cajas)
1.  En el mismo Remito, haga clic en **Imprimir**.
2.  Seleccione **"Etiquetas de Despacho (Por Caja)"**.
3.  *Resultado:* Un PDF donde cada hoja representa una caja física, ideal para pegar en el exterior del bulto.

### C. Imprimir Etiquetas de Producto (Vehículo)
1.  Puede hacerlo desde el Remito (botón **Acción > Etiquetas**) o desde la ficha del Producto.
2.  En el asistente, seleccione el formato **"Etiqueta Vehículo (Rollo)"**.
3.  *Configuración Previa:* Asegúrese de que el producto tenga asignada una **Marca de Vehículo** y un **Código de Barras**.
4.  *Resultado:* Un PDF diseñado para impresoras térmicas (100x50mm) con el logo de la empresa, el logo de la marca del auto, el código de referencia en grande y el código de barras escaneable.

---

## 📁 Estructura de Archivos

```text
stock_delivery_box_grouping/
├── __init__.py
├── __manifest__.py
├── security/
│   └── ir.model.access.csv           # Permisos para el modelo de Marcas
├── models/
│   ├── __init__.py
│   ├── stock_move.py                 # Campo box_number en Move
│   ├── stock_move_line.py            # Campo box_number en Move Line (Related)
│   ├── product_vehicle_brand.py      # Nuevo modelo de Marcas
│   ├── product_template.py           # Campos de vehículo en Producto
│   └── product_label_layout.py       # Lógica del Wizard de impresión
├── reports/
│   ├── paper_formats.xml             # Definición de tamaños (150x100, 100x50)
│   ├── stock_delivery_by_box.xml     # Diseño del Remito Agrupado
│   ├── stock_label_dispatch.xml      # Diseño de Etiqueta de Caja
│   └── product_label_vehicle.xml     # Diseño de Etiqueta de Producto (Rollo)
└── views/
    ├── stock_picking_views.xml       # Inyección de campos en vistas de Picking
    ├── product_vehicle_brand_views.xml # Menú de configuración de Marcas
    └── product_template_views.xml    # Pestaña de configuración en Producto