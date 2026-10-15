# Decisiones de Diseño — ERP Django
## Espiral 2 · Modelo Entidad-Relación

---

### D-01: Producto → Categoria usa on_delete=PROTECT

**Decisión:** No permitir borrar una categoría si tiene productos asociados.

**Alternativas consideradas:**
- CASCADE: borraría todos los productos de esa categoría.
- SET_NULL: dejaría productos sin categoría.

**Consecuencia:** Para borrar una categoría, primero se deben reasignar sus productos.

---

### D-02: Producto → Proveedor usa on_delete=SET_NULL

**Decisión:** Un producto puede existir sin proveedor asignado.

**Justificación:** Si se elimina un proveedor, los productos se conservan y quedan sin proveedor.

---

### D-03: Venta → Cliente usa on_delete=PROTECT

**Decisión:** No borrar un cliente con historial de ventas.

**Justificación:** Se conserva el historial comercial. Para dar de baja al cliente se utiliza activo=False.

---

### D-04: Venta.total es una propiedad calculada

**Decisión:** El total se calcula y no se almacena como campo de la base de datos.
**Justificación:** Almacenar `total` en la tabla `Venta` violaría la Tercera Forma Normal (3FN) por dependencia transitiva. 
---
### D-05: DetalleVenta → Producto usa on\_delete=PROTECT 
**Decisión:** No borrar productos que hayan sido vendidos históricamente. **Justificación:** Mantiene la integridad de los reportes y comprobantes de venta. 
---
### D-06: DetalleVenta.precio\_unitario es campo almacenado 
**Decisión:** Almacenar el precio del producto al momento de registrar la venta. **Justificación:** Denormalización intencional obligatoria. El precio en el catálogo de productos puede cambiar con el tiempo, pero la venta debe preservar el precio histórico al que fue cobrada. 
---
### D-07: ConfiguracionERP como singleton
**Decisión:** Garantizar una sola fila global de configuración en el sistema (siempre `pk=1`).

**Justificación:** Mantiene los datos fiscales, IVA y logo de la empresa centralizados para facturas y reportes.
