# Validador de Metadatos ICDE

Validador XML para metadatos geoespaciales colombianos según estándares ICDE.

## Estructura del Proyecto
```
mandatados_geoservicio/
├── events/
│   └── event.json
├── geo-service/
│   ├── __init__.py
│   ├── app.py
│   └── requirements.txt
├── tests/
│   ├── integration/
│   ├── unit/
│   └── __init__.py
├── .gitattributes
├── .gitignore
├── README.md
├── samconfig.toml
└── template.yaml

## Desplegar aplicación de ejemplo

El SAM CLI es una extensión de AWS CLI que permite construir y probar aplicaciones Lambda usando Docker. Requiere:

- SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Python 3 installed](https://www.python.org/downloads/)
- Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

Para desplegar la aplicación por primera vez:

```bash
sam build --use-container
sam deploy --guided
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

