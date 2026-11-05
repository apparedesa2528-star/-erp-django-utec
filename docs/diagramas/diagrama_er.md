# Diagrama Entidad-Relación — ERP Django
## Espiral 2
## Aprobación: pendiente de revisión del asesor

mermaid
erDiagram
    CATEGORIA {
        bigint id PK
        varchar nombre UK
        text descripcion
    }

    PROVEEDOR {
        bigint id PK
        varchar nombre
        varchar contacto
        varchar correo UK
        varchar telefono
        bool activo
        datetime creado
    }

    CLIENTE {
        bigint id PK
        varchar nombre
        varchar correo UK
        varchar telefono
        bool activo
        datetime creado
    }

    PRODUCTO {
        bigint id PK
        varchar nombre
        decimal precio
        int stock
        bigint categoria_id FK
        bigint proveedor_id FK
        bool activo
        datetime creado
    }

    VENTA {
        bigint id PK
        bigint cliente_id FK
        datetime fecha
        decimal total_calc "propiedad calculada"
    }

    DETALLE_VENTA {
        bigint id PK
        bigint venta_id FK
        bigint producto_id FK
        int cantidad
        decimal precio_unitario
    }

    PEDIDO {
        bigint id PK
        varchar numero_pedido UK
        bigint cliente_id FK
        varchar estado
        datetime fecha_pedido
        date fecha_entrega
        decimal total_pagado
    }

    CONFIGURACION_ERP {
        bigint id PK
        varchar nombre_empresa
        varchar rfc
        varchar moneda
        decimal iva_porcentaje
        image logo
    }

    CATEGORIA ||--o{ PRODUCTO : "clasifica"
    PROVEEDOR |o--o{ PRODUCTO : "suministra"
    CLIENTE ||--o{ VENTA : "realiza"
    CLIENTE ||--o{ PEDIDO : "genera"
    VENTA ||--|{ DETALLE_VENTA : "contiene"
    PRODUCTO ||--o{ DETALLE_VENTA : "incluido en"


## Cardinalidades

| Relación | Tipo | Descripción |
|---|---|---|
| Categoria → Producto | 1:N obligatorio | Cada producto tiene una categoría |
| Proveedor → Producto | 1:N opcional | Un producto puede no tener proveedor |
| Cliente → Venta | 1:N | Una venta pertenece a un cliente |
| Cliente → Pedido | 1:N | Un pedido pertenece a un cliente |
| Venta → DetalleVenta | 1:N obligatorio | Una venta tiene al menos un detalle |
| Producto → DetalleVenta | 1:N | Un producto puede aparecer en varias ventas |

## Notas de diseño

- Venta.total es una propiedad calculada, no un campo de la base de datos.
- DetalleVenta.precio_unitario conserva el precio histórico.
- ConfiguracionERP se manejará como singleton.
- Pedido se implementará en la Espiral 5 (W13-W15).

## Firma de aprobación

| Rol | Nombre | Fecha | Observaciones |
|---|---|---|---|
| Desarrollador | Braulio Emiliano H.P | | |
| Asesor (PO) | MC. Román Fernando López González | | |
