## 📋 Descripción General

Este módulo personaliza el **Recibo de Entrega (Remito/Delivery Slip)** para agrupar visualmente los productos según el número de caja asignado.

El objetivo es reemplazar la lista plana de productos por una estructura dividida por cajas (ej. "CAJA - 1", "CAJA - 2"), mejorando la logística de despacho y cumpliendo con el formato solicitado por el cliente. El diseño es compatible con la localización argentina (Adhoc).

---

## 🛠️ Implementación Técnica (Lo que se hizo)

### 1. Migración de Campo Studio a Código
Se detectó que existía un campo creado con Odoo Studio (`x_studio_caja`). Para garantizar robustez y trazabilidad, se definió este campo explícitamente en el código Python, manteniendo el nombre técnico para preservar los datos existentes.

*   **Modelo `stock.move` (Pestaña Operaciones):** Se agregó `x_studio_caja`.
*   **Modelo `stock.move.line` (Pestaña Operaciones Detalladas):** Se agregó `x_studio_caja`.

### 2. Lógica de Reporte "Inteligente"
El reporte estándar itera sobre las líneas de movimiento (`stock.move.line`). Sin embargo, en el flujo operativo normal, el usuario suele asignar la caja en la vista general (`stock.move`).

Para resolver esto, se implementó una lógica de cascada en el reporte QWeb:
1.  **Nivel 1 (Prioridad):** Busca si la línea de detalle tiene caja asignada.
2.  **Nivel 2 (Fallback):** Si la línea no tiene caja, busca si la operación padre (`stock.move`) tiene caja asignada.
3.  **Nivel 3 (Sin Agrupar):** Si ninguno tiene dato, se agrupa bajo la sección "SIN AGRUPAR / SUELTOS".

### 3. Diseño QWeb
*   Se hereda de `stock.report_delivery_document`.
*   Se utiliza `priority="99"` para asegurar que esta vista sobreescriba cualquier modificación realizada por módulos de terceros (como `l10n_ar_stock` de Adhoc).
*   Se oculta la tabla estándar y se reemplaza por bucles dinámicos basados en las cajas detectadas.
*   Se ajustaron márgenes (`padding`) para mejorar la legibilidad del PDF.

---

## 🚀 Flujo de Uso y Casos Soportados

Este módulo se adapta al flujo estándar de Odoo. No requiere pasos extras complejos.

### Caso A: Carga Rápida (Flujo Normal)
El usuario valida la entrega desde la pestaña **"Operaciones"**.
1.  Ingresa al Picking (Transferencia).
2.  En la línea del producto, columna **"Nro. Caja"**, escribe el número (ej. "1").
3.  Guarda y Valida.
4.  **Resultado en PDF:** El producto aparece bajo el título **"CAJA - 1"**.

### Caso B: Carga Detallada (Lotes/Series/Packs)
El usuario necesita especificar cajas diferentes para un mismo producto (ej. mitad en caja 1, mitad en caja 2) desde la pestaña **"Operaciones Detalladas"**.
1.  Ingresa al detalle de operaciones.
2.  Asigna "1" a la primera línea y "2" a la segunda línea del mismo producto.
3.  **Resultado en PDF:** El producto se divide y aparece una parte en **"CAJA - 1"** y otra en **"CAJA - 2"**.

### Caso C: Sin Asignación
El usuario olvida poner caja o es mercancía suelta.
1.  Deja el campo vacío.
2.  **Resultado en PDF:** Los items aparecen al final bajo un bloque amarillo **"SIN AGRUPAR / SUELTOS"**.

### Caso D: Impresión antes de Validar (Estado "Disponible")
El usuario imprime el remito antes de hacer clic en "Validar".
1.  El remito está en estado `assigned` (Disponible).
2.  **Resultado en PDF:** El reporte detecta que no está hecho, por lo tanto imprime la columna **"Reservado"** en lugar de "Hecho", evitando que salgan cantidades en `0.00`.

---

## 📁 Estructura del Módulo

text
stock_delivery_box_grouping/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── stock_move.py       # Campo en el modelo padre (Operaciones)
│   └── stock_move_line.py  # Campo en el modelo hijo (Detalle)
├── reports/
│   └── stock_report_delivery.xml  # Lógica de agrupación y diseño
└── views/
    └── stock_move_line_views.xml  # Input en vista detallada