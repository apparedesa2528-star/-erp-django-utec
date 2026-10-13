# Entidades y Atributos — ERP Django
## W04 · Espiral 2: Modelado de Datos y ORM

## 1. Entidad: Categoria

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria automática |
| nombre | CharField(100) | unique, not null | Evita categorías duplicadas |
| descripcion | TextField | blank=True | Descripción opcional |

## 2. Entidad: Proveedor

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria automática |
| nombre | CharField(150) | not null | Nombre del proveedor |
| contacto | CharField(100) | blank=True | Persona de contacto |
| correo | EmailField | unique, not null | Correo único |
| telefono | CharField(20) | blank=True | Teléfono opcional |
| activo | BooleanField | default=True | Permite desactivar proveedores |
| creado | DateTimeField | auto_now_add | Fecha de creación |

## 3. Entidad: Cliente

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria automática |
| nombre | CharField(150) | not null | Nombre del cliente |
| correo | EmailField | unique, not null | Correo único |
| telefono | CharField(20) | blank=True | Teléfono opcional |
| activo | BooleanField | default=True | Permite desactivar clientes |
| creado | DateTimeField | auto_now_add | Fecha de creación |

## 4. Entidad: Producto

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria automática |
| nombre | CharField(200) | not null | Nombre del producto |
| precio | DecimalField(10,2) | MinValueValidator(0) | Evita precios negativos |
| stock | IntegerField | default=0, mínimo 0 | Controla las existencias |
| categoria | ForeignKey(Categoria) | PROTECT | Protege categorías relacionadas |
| proveedor | ForeignKey(Proveedor) | SET_NULL, null=True | Permite conservar el producto sin proveedor |
| activo | BooleanField | default=True | Indica si está disponible |
| creado | DateTimeField | auto_now_add | Fecha de creación |

## 5. Entidad: Venta

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria automática |
| cliente | ForeignKey(Cliente) | PROTECT | Conserva el historial del cliente |
| fecha | DateTimeField | auto_now_add | Fecha de la venta |
| total | Propiedad calculada | No es campo de la base de datos | Suma los subtotales de los detalles |

## 6. Entidad: DetalleVenta

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria automática |
| venta | ForeignKey(Venta) | CASCADE | Elimina los detalles junto con la venta |
| producto | ForeignKey(Producto) | PROTECT | Conserva la integridad del historial |
| cantidad | PositiveIntegerField | Mínimo 1 | Cantidad de productos vendidos |
| precio_unitario | DecimalField(10,2) | not null | Conserva el precio al vender |

## 7. Entidad: Pedido

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria automática |
| numero_pedido | CharField(20) | unique | Identificador único |
| cliente | ForeignKey(Cliente) | PROTECT | Relaciona el pedido con el cliente |
| estado | CharField(20) | choices | Estado del pedido |
| fecha_pedido | DateTimeField | auto_now_add | Fecha de creación |
| fecha_entrega | DateField | null=True | Fecha de entrega opcional |
| total_pagado | DecimalField(10,2) | null=True | Importe pagado |

## 8. Entidad: ConfiguracionERP

| Atributo | Tipo Django | Restricción | Justificación |
|---|---|---|---|
| id | BigAutoField | PK, auto | Clave primaria automática |
| nombre_empresa | CharField(200) | not null | Nombre de la empresa |
| rfc | CharField(13) | blank=True | RFC opcional |
| moneda | CharField(3) | default='MXN' | Moneda del sistema |
| iva_porcentaje | DecimalField(5,2) | default=16.00 | Porcentaje de IVA |
| logo | ImageField | null=True, blank=True | Logotipo opcional |

## Conclusión

Las ocho entidades representan los elementos principales del ERP:
categorías, proveedores, clientes, productos, ventas, detalles de venta,
pedidos y configuración general.

Cada entidad cuenta con una clave primaria y atributos definidos según
su función. Las relaciones permiten mantener la integridad de los datos
y evitar duplicaciones, siguiendo los principios de normalización hasta
la Tercera Forma Normal (3FN).