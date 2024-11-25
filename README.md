# Infraestructura Colombiana de Datos Espaciales (ICDE) <> EAFIT

## Descripción General

El Instituto Geográfico Agustín Codazzi (IGAC), a través de la Infraestructura Colombiana de Datos Espaciales (ICDE), recopila y procesa cientos de datos geográficos del país. Sin embargo, actualmente carece de herramientas robustas para validar estos datos de manera eficiente.
En un mundo donde los datos geoespaciales son fundamentales para la toma de decisiones en áreas como planificación urbana, gestión ambiental y respuesta a emergencias, garantizar la calidad de esta información es un desafío crucial.

Los procesos de validación de metadatos geoespaciales son tradicionalmente manuales, lo que los hace:
- Propensos a errores
- Lentos
- Poco escalables
- 
### Problemas Identificados:
- Validar datos geográficos nuevos y existentes
- Generar estadísticas sobre la calidad de los datos
- Proporcionar herramientas automatizadas para el procesamiento de información geoespacial


### Objetivo
Diseñar e implementar una solución tecnológica que:
- Automatice la validación de metadatos
- Asegure la calidad de los datos geoespaciales
- Facilite el acceso mediante una interfaz web moderna

## Arquitectura Tecnológica

### Tecnologías Principales
- **Infraestructura en la Nube**: Amazon Web Services (AWS)
  * S3 para almacenamiento
  * Lambda para procesamiento serverless
  * EC2 para servicios de backend
  * Glue para transformación de datos
  * Athena para consultas analíticas

- **Lenguajes de Programación**: 
  * Python (backend y validación)
  * React (frontend)

### Metodología
Proyecto desarrollado siguiendo la metodología CRISP-DM:
1. Entendimiento del negocio
2. Entendimiento de los datos
3. Preparación de datos
4. Modelado
5. Evaluación
6. Despliegue
## Componentes del Sistema

### Estructura del Proyecto

El proyecto está organizado en los siguientes directorios:

- [📁 mandatados_geoservicio](./mandatados_geoservicio) - servicios geográficos mandatados
- [📁 metadatos_raster_vector](./metadatos_raster_vector) - archivos raster y vectoriales
- [📄 Presentación](./presentacion.pdf)
- [📄 Validador de Datos](./validador_datos.pdf)
- [📄 Frontend](./Frontend.pdf)

### 1. Módulo de Validación de Metadatos
- Validación de archivos XML con metadatos geoespaciales
- Verificación de criterios de calidad:
  * Consistencia lógica
  * Conformidad de metadatos
  * Resolución y referencia espacial

### 2. Pipeline de Procesamiento
- Ingesta de datos mediante triggers en AWS Lambda
- Almacenamiento en Amazon S3
- Transformación con AWS Glue
- Consultas analíticas con Amazon Athena

### 3. Microservicios
- Validación distribuida
- Procesamiento en tiempo real
- APIs RESTful para interacción

## Funcionalidades Principales

- Carga y validación automática de metadatos geoespaciales
- Análisis de completitud de campos
- Detección de anomalías
- Generación de reportes de calidad
- Interfaz web intuitiva para usuarios

## Impacto del Proyecto

- Eliminación de procesos manuales propensos a errores
- Optimización de la gestión de datos geoespaciales
- Mejora de la interoperabilidad entre entidades
- Reducción de costos operativos
- Fomento de un ecosistema geoespacial más eficiente

## Desarrollado Por

Proyecto Integrador - Maestría en Ciencia de Datos
- Juan Felipe Ortiz
- Tomás Duque
- Andrés Guerra
- Tomás Calle
- Alejandro Mc Ewen

## Contacto

Proyecto en colaboración con la Infraestructura Colombiana de Datos Espaciales (ICDE)
