# Ficha de Sistematización — Espiral 1
## ERP Django · Espiral E1: Infraestructura y Configuración Base
## UTEC Celaya · Técnico en Programación (SEP 3061300006-23)

| Campo | Contenido |
|---|---|
| **Número de espiral** | 1 |
| **Nombre del ciclo** | Infraestructura y Configuración Base |
| **Semanas** | W01 – W03 |
| **Fecha de inicio** | 22/09/2026 |
| **Fecha de cierre** | 08/10/2026 |
| **Responsable** | [Ana Paulina Paredes Alvarado] |
| **Asesor** | MC. Román Fernando López González |

---

## 1. Objetivo del ciclo

Establecer el entorno de desarrollo portable en USB y desplegar el
proyecto Django base en Render.com, de modo que cualquier avance
posterior tenga una URL pública verificable desde el inicio del proyecto.

---

## 2. Tareas realizadas

| # | Tarea | Estado | Tiempo invertido |
|---|---|---|---|
| 1 | Configurar Python 3.11 embeddable en USB | ✅ | 1:30h  |
| 2 | Instalar pip y virtualenv | ✅ | 0:45h |
| 3 | Configurar Git Portable | ✅ | 0:30 h |
| 4 | Crear scripts iniciar/finalizar sesión | ✅ | 0:45h |
| 5 | Crear proyecto Django con 5 apps | ✅ | 1:00h |
| 6 | Sistema de templates Fable 5 AzulERP | ✅ | 1:30h |
| 7 | Configurar WhiteNoise y estáticos | ✅ | 0:45h |
| 8 | Completar settings_prod.py con PostgreSQL | ✅ | 0:45h |
| 9 | Crear Procfile, Dockerfile, docker-compose.yml | ✅ | 1:00h|
| 10 | Crear render.yaml | ✅ | 1:30h |
| 11 | Desplegar en Render.com → URL pública | ✅ | 0:30h |
| 12 | Ejecutar Sprint 0 Review y Retrospectiva | ✅ | 0:30h  |

---

## 3. Evidencias generadas

- [ ] Repositorio GitHub: `https://github.com/tu-usuario/erp-django-utec`
- [ ] URL pública Render: `https://erp-django-utec.onrender.com`
- [ ] Captura de pantalla: `evidencias/espiral_01/render_url.png`
- [ ] Captura de pantalla: `evidencias/espiral_01/manage_check.png`
- [ ] Resultado de tests: `Ran 33 tests in X.XXXs — OK`
- [ ] Commit de cierre: 
a1b2c3d Sprint 0 CIERRE [M1]: Render.com desplegado + 35 tests OK + Ficha Schmelkes E1


---

## 4. Criterios de aceptación verificados

| Criterio | ¿Cumplido? | Evidencia |
|---|---|---|
| `manage.py check --deploy` sin warnings críticos | ✅ | Verificado en terminal |
| URL pública `https://…onrender.com/` → HTTP 200 | ✅  | Captura del navegador |
| Repositorio con ≥ 6 commits en rama `main` | ✅  | `git log --oneline` |
| 33 tests pasando (W01 + W02 + W03) | ✅  | 35 tests OK |
| Ficha Schmelkes E1 completa | ✅ | Este documento |

---

## 5. Problemas encontrados y soluciones
 | Problema | Causa | Solución aplicada |
  |---|---|---|
| Error `UnicodeDecodeError` al leer `requirements.txt` | El archivo se guardó con codificación UTF-16 LE / BOM en Windows | Se reguardó `requirements.txt` con codificación UTF-8 pura en VS Code |
| Fallo en test por typo `psycop2-binary` | Error tipográfico al escribir el nombre del paquete | Se corrigió la línea a `psycopg2-binary&gt;=2.9.9` |
| Error `No such file or directory: requirements.txt` en Render | Docker no encontraba el archivo por regla en `.dockerignore` | Se ajustó `.dockerignore` para permitir la copia de `requirements.txt` en la imagen |
---

## 6. Lecciones aprendidas

1.Siempre verificar que los archivos de configuración (`requirements.txt`, `Dockerfile`, `Procfile`) estén en la raíz y en codificación UTF-8 sin BOM.

2.Hacer commits atómicos y descriptivos facilita rastrear la causa exacta cuando un despliegue en PaaS (Render) falla.

3.Probar la suite de tests unitarios antes de subir a producción asegura que los cambios no rompan la arquitectura base.

---

## 7. Tiempo total invertido
  | Categoría | Horas |
|---|---|
| Diseño / planeación | 2.0 h |
| Implementación | 7.5 h |
| Pruebas | 1.5 h |
| Despliegue | 2.0 h |
| Documentación | 1.0 h |
| **Total Espiral 1** | **14.0 h** | ---  |

---

## 8. Conexión con el trabajo recepcional

> Esta espiral aporta evidencia para el **Capítulo 4** (Desarrollo),
> sección 4.1 "Espiral 1: Infraestructura", y para el
> **Capítulo 3** (Metodología), subsección "Ciclos del modelo espiral".
### 2. sprint0_retrospective.md
 Este archivo registra el análisis de proceso del Sprint 0 [2, 4]:markdown 
 # Sprint 0 Retrospective — ERP Django 
 ## Semanas W01–W03 · Espiral 1 Fecha: 08/10/2026 Facilitador/Scrum Master:
 Ana Paulina Paredes Alvarado
 ## ¿Qué funcionó bien? (Keep) 
 1. Uso del entorno portable en USB para mantener el código sincronizado entre la escuela y la casa. 
 2. La ejecución constante de la suite de pruebas unitarias (python manage.py test tests). 
 3. El despliegue continuo conectado directamente al repositorio de GitHub. 
 ## ¿Qué mejorar? (Improve) 
 1. Verificar la codificación de archivos de texto en Windows antes de subirlos a GitHub. 
 2. Hacer commits más seguidos durante la clase para no acumular demasiados cambios al final. 
 ## ¿Qué eliminar? (Drop) 
 1. Crear o editar archivos de configuración crítica mediante herramientas que modifiquen la codificación (como Notepad sin UTF-8). 
 ## Acción de mejora (Kaizen) para Sprint 1 &gt; 
 En el Sprint 1, voy a realizar verificaciones con type o en VS Code antes de cada git push para asegurar que los archivos nuevos estén correctamente guardados en UTF-8. 
 ## Velocidad del Sprint 0 | HU | Planificado (pts) | Entregado (pts) |
|---|---|---| 
| HU-E1-01 Entorno portable | 3 | 3 | 
| HU-E1-02 Scripts sincronización | 2 | 2 | 
| HU-E1-03 Repositorio GitHub | 2 | 2 | 
| HU-E1-04 Despliegue Render.com | 3 | 3 | 
| **Total** | **10** | **10** | 
**Velocidad real del equipo:** 10 puntos / sprint
