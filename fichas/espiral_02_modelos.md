# Espiral 02 — Modelado de Datos y ORM
## Proyecto ERP Django
### Semana W04

---

## 1. Objetivo

Identificar las entidades del sistema ERP, definir sus atributos,
establecer las relaciones entre ellas y documentar las decisiones
de diseño aplicando los principios de normalización hasta la
Tercera Forma Normal (3FN).

## 2. Entidades identificadas

El sistema ERP contempla las siguientes ocho entidades:

1. Categoria
2. Proveedor
3. Cliente
4. Producto
5. Venta
6. DetalleVenta
7. Pedido
8. ConfiguracionERP

Los atributos, tipos de datos y restricciones se documentan en:

`docs/entidades_atributos.md`

## 3. Relaciones entre entidades

| Entidad principal | Entidad relacionada | Cardinalidad |
|---|---|---|
| Categoria | Producto | 1:N |
| Proveedor | Producto | 1:N opcional |
| Cliente | Venta | 1:N |
| Cliente | Pedido | 1:N |
| Venta | DetalleVenta | 1:N |
| Producto | DetalleVenta | 1:N |

Las relaciones se representan mediante claves foráneas y deben
mantener la integridad de los datos.

## 4. Normalización

El diseño busca cumplir con la Tercera Forma Normal (3FN).

- Cada entidad cuenta con una clave primaria.
- Los datos de categorías, clientes y proveedores se almacenan
  en sus propias entidades.
- Los productos hacen referencia a sus categorías y proveedores.
- Los detalles de venta conservan el precio histórico del producto.
- El total de una venta se plantea como una propiedad calculada.

## 5. Decisiones de diseño

Las decisiones de diseño se documentan en:

`docs/decisiones_diseno.md`

Se consideran las siguientes reglas:

- Producto → Categoria: PROTECT.
- Producto → Proveedor: SET_NULL.
- Venta → Cliente: PROTECT.
- DetalleVenta → Producto: PROTECT.
- Venta.total: propiedad calculada.
- DetalleVenta.precio_unitario: dato histórico.
- ConfiguracionERP: configuración global única.

Estas reglas deberán implementarse y comprobarse en la etapa
de desarrollo correspondiente.

## 6. Diagrama entidad-relación

El diagrama Mermaid se encuentra en:

`docs/diagramas/diagrama_er.md`

La versión visual exportada desde dbdiagram.io se guarda en:

`evidencias/espiral_02/diagrama_er.png`

El diagrama representa las ocho entidades y sus relaciones.

## 7. Evidencias

| Evidencia | Ruta |
|---|---|
| Entidades y atributos | docs/entidades_atributos.md |
| Decisiones de diseño | docs/decisiones_diseno.md |
| Diagrama Mermaid | docs/diagramas/diagrama_er.md |
| Diagrama exportado | evidencias/espiral_02/diagrama_er.png |

## 8. Pruebas y validación

En esta etapa se revisa la documentación y el diseño del modelo.

- [ ] Las ocho entidades están documentadas.
- [ ] Los atributos tienen tipos de datos definidos.
- [ ] Las claves primarias y foráneas están identificadas.
- [ ] Las cardinalidades están representadas correctamente.
- [ ] Se documentaron las decisiones de diseño.
- [ ] Se revisó la normalización 3FN.
- [ ] Se generó el diagrama visual.
- [ ] Se guardó la evidencia.

Las pruebas automatizadas de los modelos se realizarán cuando
corresponda implementar el ORM en la siguiente etapa.

## 9. Conclusión

La Espiral 02 establece la estructura conceptual y relacional
de los datos del ERP. La documentación permite definir las
entidades, sus atributos y sus relaciones antes de implementar
los modelos en Django.

## 10. Estado de aprobación

Estado: Pendiente de revisión del asesor.

Fecha de revisión: 08-10-26

Observaciones:
____________________________________________________

Nombre del estudiante: Ana Paulina Paredes Alvarado

Nombre del asesor: Roman Fernando Lopez Gonzales