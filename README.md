# Prueba de Desempeño - Proyecto de Análisis de Datos

## Descripción General

Este proyecto implementa un pipeline de procesamiento de datos ETL (Extract, Transform, Load) para análisis de desempeño. Utiliza un enfoque de arquitectura de medallón con capas de datos (bronce, plata, oro) para garantizar la calidad y trazabilidad de los datos.

## Estructura del Proyecto

```
prueba_desempeño/
├── README.md                 # Esta documentación
├── requirements.txt          # Dependencias del proyecto
├── data/
│   └── 01_bronce/           # Capa bronce (datos crudos)
│       └── dataset.csv      # Dataset fuente para análisis
└── scripts/
    ├── extract_transform.py # Script de extracción y transformación
    └── load.py              # Script de carga de datos
```

## Tecnologías y Dependencias

El proyecto utiliza las siguientes librerías Python:

| Librería                   | Versión | Propósito                                              |
| --------------------------- | -------- | ------------------------------------------------------- |
| **greenlet**          | 3.5.5    | Primitiva de concurrencia ligera para operaciones async |
| **numpy**             | 2.5.2    | Computación numérica y operaciones con arrays         |
| **pandas**            | 3.0.5    | Manipulación y análisis de datos                      |
| **psycopg2-binary**   | 2.9.12   | Adaptador PostgreSQL para Python                        |
| **python-dateutil**   | 2.9.0    | Utilidades para manejo de fechas y tiempos              |
| **six**               | 1.17.0   | Utilidades de compatibilidad Python 2/3                 |
| **SQLAlchemy**        | 2.0.52   | ORM y toolkit SQL                                       |
| **typing_extensions** | 4.16.0   | Extensiones de tipado para Python                       |
| **tzdata**            | 2026.3   | Base de datos de zonas horarias                         |

## Componentes del Proyecto

### Capa de Datos

- **01_bronce/**: Capa bronce que contiene los datos crudos originales sin procesar
  - `dataset.csv`: Dataset fuente con los datos originales para análisis

### Scripts de Procesamiento

1. **extract_transform.py**

   - Realiza la extracción de datos desde la fuente (CSV)
   - Aplica transformaciones de limpieza y normalizacion
   - Prepara datos para la carga en la base de datos
   - Implementa validaciones de calidad de datos
2. **load.py**

   - Carga los datos transformados en la base de datos
   - Utiliza SQLAlchemy para operaciones ORM
   - Conecta a PostgreSQL mediante psycopg2
   - Gestiona transacciones y manejo de errores

## Instalación y Configuración

### Requisitos Previos

- Python 3.7 o superior
- PostgreSQL (para la carga de datos)
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Crear un entorno virtual**

   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```
2. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar variables de entorno**

   - Crear archivo `.env` con credenciales de base de datos
   - Configurar parámetros de conexión PostgreSQL

## ▶️ Ejecución

### Ejecutar el Pipeline ETL

1. **Extracción y Transformación**

   ```bash
   python scripts/extract_transform.py
   ```
2. **Carga de Datos**

   ```bash
   python scripts/load.py
   ```
3. **Ejecutar el pipeline completo**

   ```bash
   python scripts/extract_transform.py && python scripts/load.py
   ```

## ❓ Preguntas de Negocio


¿se logro la venta anual y mensual respecto a mes anterior?
¿Las categorias más vendidas?
¿impacto de las ventas de descuentos
¿donde vendo esa estrategia?
¿por que medio de pago sale más rentable?

## 📊 Arquitectura de Datos - Medallón

El proyecto implementa una arquitectura de medallón de tres capas:

### Capa Bronce (Bronze)

- Almacena datos crudos sin procesar
- Fuente: Archivos CSV
- Propósito: Histórico y auditoría completa de datos originales

### Capa Plata (Silver)

- Datos transformados y limpios
- Validaciones aplicadas
- Propósito: Datos confiables para análisis

### Capa Oro (Gold)

- Datos procesados y agregados
- Modelos de datos finales
- Propósito: Consultas y reportes de negocio

## Características de Seguridad

- Utiliza psycopg2-binary para conexiones seguras a PostgreSQL
- SQLAlchemy para prevenir inyecciones SQL
- Gestión de credenciales mediante variables de entorno
- Trazabilidad completa de transformaciones de datos
