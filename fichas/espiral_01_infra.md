# Ficha de Sistematización — Espiral 1

## ERP Django · Espiral E1: Infraestructura y Configuración Base

**UTEC Celaya · Técnico en Programación (SEP 3061300006-23)**

| Campo                 | Contenido                            |
| --------------------- | ------------------------------------ |
| **Número de espiral** | 1                                    |
| **Nombre del ciclo**  | Infraestructura y Configuración Base |
| **Semanas**           | W01 – W03                            |
| **Fecha de inicio**   | 22/09/2026                           |
| **Fecha de cierre**   | 08/10/2026                           |
| **Responsable**       | Braulio Emiliano Hernandez peña      |
|**Grado y grupo**      | 3J                                   |
| **Asesor**            | MC. Román Fernando López González    |
---

## 1. Objetivo del ciclo

Establecer el entorno de desarrollo portable en USB y desplegar el proyecto Django base en Render.com, de modo que cualquier avance posterior tenga una URL pública verificable desde el inicio del proyecto.

---

## 2. Tareas realizadas

| #  | Tarea                                                 | Estado | Tiempo invertido |
| -- | ----------------------------------------------------- | ------ | ---------------- |
| 1  | Configurar Python 3.11 embeddable en USB              | ✅      | 1:30h           |
| 2  | Instalar pip y virtualenv                             | ✅      | 0:45h           |
| 3  | Configurar Git Portable                               | ✅      | 0:30h           |
| 4  | Crear scripts iniciar/finalizar sesión                | ✅      | 0:45h           |
| 5  | Crear proyecto Django con 5 apps                      | ✅      | 1:00h           |
| 6  | Sistema de templates Fable 5 AzulERP                  | ✅      | 1:30h           |
| 7  | Configurar WhiteNoise y archivos estáticos            | ✅      | 0:45h           |
| 8  | Completar `settings_prod.py` con PostgreSQL           | ✅      | 1:00h           |
| 9  | Crear `Procfile`, `Dockerfile` y `docker-compose.yml` | ✅      | 1:00h           |
| 10 | Crear `render.yaml`                                   | ✅      | 0:30h           |
| 11 | Desplegar en Render.com → URL pública                 | ✅      | 2:00h           |
| 12 | Ejecutar Sprint 0 Review y Retrospectiva              | ✅      | 0:45h           |

---

## 3. Evidencias generadas
 - [x] **Repositorio GitHub:** `https://github.com/poyiyiyinis/erp-django-utec` [4] 
 - [x] **URL pública Render:** `https://erp-django-utec.onrender.com` [5] 
 - [x] **Capturas de pantalla:** Guardadas en `evidencias/espiral_01/` [5] 
 - [x] **Resultado de tests:** `Ran 33 tests in 0.050s — OK` [5, 6] 
 - [x] **Commit de cierre:** `Sprint 0 CIERRE [M1]: Render.com desplegado + 33 tests OK + Ficha Schmelkes E1` [7, 8]
## 4. Criterios de aceptación verificados
 | Criterio | ¿Cumplido? | Evidencia |
|---|---|---|
| `manage.py check --deploy` sin warnings críticos | ✅ |Verificado en consola de Render | 
| URL pública `https://…onrender.com` → HTTP 200 | ✅ | Acceso web a módulos ERP | 
| Repositorio con ≥ 6 commits en rama `main` | ✅ | Historial `git log --oneline` | | 33 tests pasando (W01 + W02 + W03) | ✅ | Suite de pruebas ejecutada OK | | Ficha Schmelkes E1 completa | ✅ | Este documento |

## 5. Problemas encontrados y soluciones
| Problema | Causa | Solución aplicada |
|---|---|---|
| Error `UnicodeDecodeError` al leer `requirements.txt` | El archivo se guardó con codificación UTF-16 LE / BOM en Windows | Se reguardó `requirements.txt` con codificación UTF-8 pura en VS Code |
| Fallo en test por typo `psycop2-binary` | Error tipográfico al escribir el nombre del paquete | Se corrigió la línea a `psycopg2-binary&gt;=2.9.9` |
| Error `No such file or directory: requirements.txt` en Render | Docker no encontraba el archivo por regla en `.dockerignore` | Se ajustó `.dockerignore` para permitir la copia de `requirements.txt` en la imagen |

## 6. Lecciones aprendidas

 1. En entornos Linux (como los contenedores de Render), los nombres de archivos son estrictamente sensibles a mayúsculas y minúsculas (*case-sensitive*). 
 2. Es indispensable guardar todos los archivos de configuración y requerimientos en codificación **UTF-8 sin BOM** para evitar fallos de lectura en Python. 3. Configurar el despliegue continuo desde el inicio (Espiral 1) garantiza que los errores de integración se detecten de inmediato antes de agregar complejidad de lógica de negocio.
 ---
## 7. Tiempo total invertido
| Categoría | Horas |
|---|---|
| Diseño / planeación | 2.0 h |
| Implementación | 7.5 h |
| Pruebas | 1.5 h |
| Despliegue | 2.0 h |
| Documentación | 1.0 h |
| **Total Espiral 1** | **14.0 h** | ---

## 8. Conexión con el trabajo recepcional
&gt; Esta espiral aporta evidencia para el **Capítulo 4** (Desarrollo), sección    
4.1 "Espiral 1: Infraestructura", y para el **Capítulo 3** (Metodología), subsección "Ciclos del modelo espiral" [2].
