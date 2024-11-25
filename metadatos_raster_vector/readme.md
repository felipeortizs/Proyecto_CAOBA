# Validador de Metadatos ICDE

Validador XML para metadatos geoespaciales colombianos según estándares ICDE.

## Estructura del Proyecto
```
metadatos_raster_vector/
├── metadatos/
│   ├── raster/          # XMLs de metadatos raster 
│   └── vector/          # XMLs de metadatos vector
├── serverless_lambda.py # Código función Lambda AWS
├── main.ipynb          # Notebook para pruebas locales
└── README.md
```

## Instalación Local
```bash
pip install boto3
```

## Uso Local
```python
python main.ipynb
```

## Despliegue en AWS Lambda

### Requisitos
- Cuenta AWS activa
- Código fuente en ZIP
- Permisos IAM

### Implementación
1. **Crear Lambda**
- AWS Console > Lambda
- "Crear función" > "Crear desde cero"
- Nombre: `metadata-validator`
- Runtime: Python 3.9
- Arquitectura: x86_64

2. **Permisos IAM**
- AWSLambdaBasicExecutionRole
- S3FullAccess

3. **Código**
- Subir ZIP
- Handler: `serverless_lambda.lambda_handler`

4. **Recursos**
- Memoria: 256 MB
- Timeout: 30s

5. **API Gateway**
- Crear API REST
- Recurso `/validate`
- Método POST
- Integrar con Lambda
- Desplegar

## Análisis con AWS Glue y Athena

### Consultas SQL para Análisis de Datos

1. **Distribución de Calidad por Tipo**
```sql
SELECT 
    CASE 
        WHEN CAST(completeness_percentage AS double) >= 90 THEN 'Excelente (90-100%)'
        WHEN CAST(completeness_percentage AS double) >= 80 THEN 'Bueno (80-89%)'
        WHEN CAST(completeness_percentage AS double) >= 70 THEN 'Regular (70-79%)'
        ELSE 'Deficiente (<70%)'
    END as rango_calidad,
    metadata_type,
    COUNT(*) as cantidad
FROM "icde"."metrics"
GROUP BY 
    CASE 
        WHEN CAST(completeness_percentage AS double) >= 90 THEN 'Excelente (90-100%)'
        WHEN CAST(completeness_percentage AS double) >= 80 THEN 'Bueno (80-89%)'
        WHEN CAST(completeness_percentage AS double) >= 70 THEN 'Regular (70-79%)'
        ELSE 'Deficiente (<70%)'
    END,
    metadata_type
ORDER BY metadata_type, rango_calidad;
```

2. **Análisis Mensual de Completitud**
```sql
SELECT 
    DATE_TRUNC('month', parse_datetime(SUBSTRING(timestamp, 1, 19),'yyyy-MM-dd''T''HH:mm:ss')) as mes,
    metadata_type,
    AVG(CAST(completeness_percentage AS double)) as promedio_completitud,
    COUNT(*) as total_registros
FROM "icde"."metrics"
GROUP BY 
    DATE_TRUNC('month', parse_datetime(SUBSTRING(timestamp, 1, 19),'yyyy-MM-dd''T''HH:mm:ss')), 
    metadata_type
ORDER BY mes DESC;
```

3. **Estadísticas por Tipo de Metadato**
```sql
SELECT 
    metadata_type,
    COUNT(*) as total_validaciones,
    ROUND(AVG(CAST(completeness_percentage AS double)), 2) as promedio_completitud,
    ROUND(MIN(CAST(completeness_percentage AS double)), 2) as min_completitud,
    ROUND(MAX(CAST(completeness_percentage AS double)), 2) as max_completitud,
    ROUND(STDDEV_POP(CAST(completeness_percentage AS double)), 2) as desviacion_estandar,
    ROUND(AVG(CAST(total_fields AS double)), 0) as promedio_campos_totales,
    ROUND(AVG(CAST(missing_fields_count AS double)), 0) as promedio_campos_faltantes
FROM "icde"."metrics"
GROUP BY metadata_type;
```

4. **Top Campos Problemáticos por Tipo**
```sql
SELECT 
    m.metadata_type,
    f.field_name,
    COUNT(*) as frecuencia_faltante,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY m.metadata_type), 2) as porcentaje_del_tipo
FROM "icde"."fields" f
JOIN "icde"."metrics" m 
    ON f.validation_id = m.id
WHERE f.field_status = 'missing'
GROUP BY m.metadata_type, f.field_name
HAVING COUNT(*) > 1
ORDER BY frecuencia_faltante DESC
LIMIT 20;
```

5. **Análisis de Secciones con Más Problemas**
```sql
SELECT 
    SPLIT_PART(f.field_name, '.', 1) as seccion_principal,
    m.metadata_type,
    COUNT(*) as total_campos,
    SUM(CASE WHEN f.field_status = 'missing' THEN 1 ELSE 0 END) as campos_faltantes,
    ROUND(SUM(CASE WHEN f.field_status = 'missing' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as porcentaje_faltante
FROM "icde"."fields" f
JOIN "icde"."metrics" m 
    ON f.validation_id = m.id
GROUP BY 
    SPLIT_PART(f.field_name, '.', 1),
    m.metadata_type
HAVING COUNT(*) > 0
ORDER BY porcentaje_faltante DESC;
```

## Fuentes de Datos
- [Catálogo ICDE](https://metadatos.icde.gov.co/geonetwork/srv/spa/catalog.search#/home)
- [Visualizador IDEAM](https://visualizador.ideam.gov.co/geonetwork/srv/spa/catalog.search)
- [Catálogo UPRA](https://catalogometadatos.upra.gov.co/uprageonet/srv/spa/catalog.search#/home)

## Funcionalidades
- Validación XML para datos raster/vector
- Extracción según ISO 19115-1:2014
- Métricas y reportes de validación
- Almacenamiento en S3
- Análisis con AWS Glue y Athena
- Despliegue local y serverless

## Pruebas
- URL API Gateway
- Método POST
- XML en body
- Verificar respuesta JSON

## Notas
- Configurar CORS
- Monitorear con CloudWatch
- Revisar límites de tamaño de payload

## Licencia
MIT