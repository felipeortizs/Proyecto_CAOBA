import json
import xml.etree.ElementTree as ET
import base64
from typing import Dict, List, Tuple
import boto3
import datetime

def save_validation_metrics(metrics_data: dict, metadata_type: str) -> str:
    """
    Guarda las métricas de validación en un archivo CSV en S3
    
    Args:
        metrics_data (dict): Diccionario con las métricas de validación
        metadata_type (str): Tipo de metadato (vector/grid)
    
    Returns:
        str: URL del archivo CSV en S3
    """
    try:
        import csv
        import io
        import boto3
        from datetime import datetime
        
        # Crear contenido CSV en memoria
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        
        # Escribir encabezados
        writer.writerow([
            'id',
            'timestamp',
            'metadata_type',
            'completeness_percentage',
            'total_fields',
            'completed_fields_count',
            'missing_fields_count'
        ])
        
        # Generar ID único para relacionar los registros
        validation_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Escribir datos
        writer.writerow([
            validation_id,
            datetime.now().isoformat(),
            metadata_type,
            metrics_data['completeness_percentage'],
            metrics_data['total_fields'],
            metrics_data['completed_fields_count'],
            metrics_data['missing_fields_count']
        ])
        
        # Configurar cliente S3
        s3_client = boto3.client('s3')
        bucket_name = 'proyecto-integrador-icde'
        
        # Generar nombre del archivo
        file_key = f"processed/metrics/validation_metrics_{validation_id}.csv"
        
        # Subir CSV a S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
        
        return validation_id, f"s3://{bucket_name}/{file_key}"
        
    except Exception as e:
        print(f"Error guardando métricas en S3: {str(e)}")
        raise e

def save_validation_fields(fields_data: dict, validation_id: str, metadata_type: str) -> str:
    """
    Guarda los campos de validación en un archivo CSV en S3
    
    Args:
        fields_data (dict): Diccionario con los campos completos y faltantes
        validation_id (str): ID de validación para relacionar con las métricas
        metadata_type (str): Tipo de metadato (vector/grid)
    
    Returns:
        str: URL del archivo CSV en S3
    """
    try:
        import csv
        import io
        import boto3
        from datetime import datetime
        
        # Crear contenido CSV en memoria
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        
        # Escribir encabezados
        writer.writerow([
            'validation_id',
            'timestamp',
            'metadata_type',
            'field_name',
            'field_status'  # 'complete' o 'missing'
        ])
        
        # Escribir campos completos
        for field in fields_data['complete_fields']:
            writer.writerow([
                validation_id,
                datetime.now().isoformat(),
                metadata_type,
                field,
                'complete'
            ])
            
        # Escribir campos faltantes
        for field in fields_data['missing_fields']:
            writer.writerow([
                validation_id,
                datetime.now().isoformat(),
                metadata_type,
                field,
                'missing'
            ])
        
        # Configurar cliente S3
        s3_client = boto3.client('s3')
        bucket_name = 'proyecto-integrador-icde'
        
        # Generar nombre del archivo
        file_key = f"processed/fields/validation_fields_{validation_id}.csv"
        
        # Subir CSV a S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
        
        return f"s3://{bucket_name}/{file_key}"
        
    except Exception as e:
        print(f"Error guardando campos en S3: {str(e)}")
        raise e

def save_to_s3(xml_content: str, metadata_type: str) -> str:
    """
    Guarda el XML en S3 y retorna la URL
    """
    try:
        s3_client = boto3.client('s3')
        bucket_name = 'proyecto-integrador-icde'
        
        # Generar nombre único para el archivo
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_key = f"metadata/{metadata_type}/{timestamp}.xml"
        
        # Guardar el XML en S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=xml_content,
            ContentType='application/xml'
        )
        
        # Generar URL del archivo
        url = f"s3://{bucket_name}/{file_key}"
        return url
        
    except Exception as e:
        print(f"Error guardando en S3: {str(e)}")
        raise e

class MetadataExtractor:
    """Clase base para la extracción de metadatos"""
    
    def __init__(self):
        self.namespaces = {
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gco': 'http://www.isotc211.org/2005/gco',
            'gts': 'http://www.isotc211.org/2005/gts',
            'gml': 'http://www.opengis.net/gml/3.2',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }

    def get_element_text(self, element, xpath):
        """Extrae el texto de un elemento XML"""
        elem = element.find(xpath, self.namespaces)
        if elem is not None:
            return elem.text
        return None

    def get_code_list_value(self, element, xpath):
        """Obtiene el valor de una lista de códigos"""
        elem = element.find(xpath, self.namespaces)
        if elem is not None:
            return elem.get('codeListValue')
        return None

    def extract_common_metadata(self, root):
        """Extrae los metadatos comunes para todos los tipos"""
        metadata = {
            'metadato': {
                'codigo': self.get_element_text(root, './/gmd:fileIdentifier/gco:CharacterString'),
                'idioma': self.get_element_text(root, './/gmd:language/gco:CharacterString'),
                'codificacion': self.get_code_list_value(root, './/gmd:characterSet/gmd:MD_CharacterSetCode'),
                'contacto': self.extract_contact_info(root.find('.//gmd:contact/gmd:CI_ResponsibleParty', self.namespaces)),
                'fecha': self.extract_date_info(root.find('.//gmd:dateStamp', self.namespaces)),
                'norma': {
                    'nombre': self.get_element_text(root, './/gmd:metadataStandardName/gco:CharacterString'),
                    'version': self.get_element_text(root, './/gmd:metadataStandardVersion/gco:CharacterString')
                },
                'perfil': {
                    'nombre': self.get_element_text(root, './/gmd:metadataProfileName/gco:CharacterString'),
                    'version': None  # Opcional
                },
                'ambito': self.get_code_list_value(root, './/gmd:hierarchyLevel/gmd:MD_ScopeCode')
            },
            'identificacion': self.extract_identification_info(root)
        }
        return metadata

    def extract_contact_info(self, contact_element):
        """Extrae la información de contacto"""
        if contact_element is None:
            return None
            
        return {
            'rol': self.get_code_list_value(contact_element, './/gmd:role/gmd:CI_RoleCode'),
            'organizacion': self.get_element_text(contact_element, './/gmd:organisationName/gco:CharacterString'),
            'cargo': self.get_element_text(contact_element, './/gmd:positionName/gco:CharacterString'),
            'telefono': {
                'numero': self.get_element_text(contact_element, './/gmd:voice/gco:CharacterString'),
                'tipo': self.get_code_list_value(contact_element, './/gmd:CI_TelephoneTypeCode')
            },
            'direccion': self.get_element_text(contact_element, './/gmd:deliveryPoint/gco:CharacterString'),
            'ciudad': self.get_element_text(contact_element, './/gmd:city/gco:CharacterString'),
            'pais': self.get_element_text(contact_element, './/gmd:country/gco:CharacterString'),
            'email': self.get_element_text(contact_element, './/gmd:electronicMailAddress/gco:CharacterString'),
            'enlace': self.get_element_text(contact_element, './/gmd:linkage/gmd:URL')
        }

    def extract_date_info(self, date_element):
        """Extrae la información de fecha"""
        if date_element is None:
            return None
            
        return {
            'valor': self.get_element_text(date_element, './/gco:DateTime') or 
                    self.get_element_text(date_element, './/gco:Date'),
            'tipo': self.get_code_list_value(date_element, './/gmd:CI_DateTypeCode')
        }

    def extract_identification_info(self, root):
        """Extrae la información de identificación común"""
        ident = root.find('.//gmd:identificationInfo/gmd:MD_DataIdentification', self.namespaces)
        if ident is None:
            return None

        extent = ident.find('.//gmd:extent//gmd:EX_GeographicBoundingBox', self.namespaces)
        return {
            'titulo': self.get_element_text(ident, './/gmd:citation//gmd:title/gco:CharacterString'),
            'fecha': self.extract_date_info(ident.find('.//gmd:citation//gmd:date', self.namespaces)),
            'resumen': self.get_element_text(ident, './/gmd:abstract/gco:CharacterString'),
            'contacto': self.extract_contact_info(ident.find('.//gmd:pointOfContact/gmd:CI_ResponsibleParty', self.namespaces)),
            'tipo_representacion': self.get_code_list_value(ident, './/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode'),
            'categoria_tema': self.get_code_list_value(ident, './/gmd:topicCategory/gmd:MD_TopicCategoryCode'),
            'extension': self.extract_extent_info(extent),
            'mantenimiento': {
                'frecuencia': self.get_code_list_value(ident, './/gmd:resourceMaintenance//gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode')
            },
            'palabras_clave': self.extract_keywords(ident)
        }

    def extract_extent_info(self, extent):
        """Extrae la información de extensión geográfica"""
        if extent is None:
            return None
            
        return {
            'oeste': self.get_element_text(extent, './/gmd:westBoundLongitude/gco:Decimal'),
            'este': self.get_element_text(extent, './/gmd:eastBoundLongitude/gco:Decimal'),
            'sur': self.get_element_text(extent, './/gmd:southBoundLatitude/gco:Decimal'),
            'norte': self.get_element_text(extent, './/gmd:northBoundLatitude/gco:Decimal')
        }

    def extract_keywords(self, ident):
        """Extrae las palabras clave"""
        keywords = []
        for keyword in ident.findall('.//gmd:keyword/gco:CharacterString', self.namespaces):
            if keyword.text:
                keywords.append(keyword.text)
        return keywords

class VectorMetadataExtractor(MetadataExtractor):
    """Extractor específico para metadatos de tipo vector"""

    def extract(self, root):
        metadata = self.extract_common_metadata(root)
        vector_specific = {
            'vector_info': {
                'nivel_topologia': self.get_element_text(root, './/gmd:topologyLevel/gco:CharacterString'),
                'objetos_geometricos': self.extract_geometric_objects(root),
                'denominador_escala': self.get_element_text(root, './/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer')
            }
        }
        metadata.update(vector_specific)
        return metadata

    def extract_geometric_objects(self, root):
        """Extrae información sobre objetos geométricos"""
        objects = []
        for obj in root.findall('.//gmd:geometricObjects/gmd:MD_GeometricObjects', self.namespaces):
            objects.append({
                'tipo': self.get_code_list_value(obj, './/gmd:geometricObjectType/gmd:MD_GeometricObjectTypeCode'),
                'cantidad': self.get_element_text(obj, './/gmd:geometricObjectCount/gco:Integer')
            })
        return objects

class RasterMetadataExtractor(MetadataExtractor):
    """Extractor específico para metadatos de tipo raster"""

    def extract(self, root):
        metadata = self.extract_common_metadata(root)
        raster_specific = {
            'raster_info': {
                'numero_dimensiones': self.get_element_text(root, './/gmd:numberOfDimensions/gco:Integer'),
                'dimensiones': self.extract_dimensions(root),
                'geometria_celda': self.get_code_list_value(root, './/gmd:cellGeometry/gmd:MD_CellGeometryCode'),
                'imagen': self.extract_image_description(root)
            }
        }
        metadata.update(raster_specific)
        return metadata

    def extract_dimensions(self, root):
        """Extrae información sobre las dimensiones"""
        dimensions = []
        for dim in root.findall('.//gmd:axisDimensionProperties/gmd:MD_Dimension', self.namespaces):
            dimensions.append({
                'nombre': self.get_code_list_value(dim, './/gmd:dimensionName/gmd:MD_DimensionNameTypeCode'),
                'tamaño': self.get_element_text(dim, './/gmd:dimensionSize/gco:Integer'),
                'resolucion': self.get_element_text(dim, './/gmd:resolution/gco:Measure')
            })
        return dimensions

    def extract_image_description(self, root):
        """Extrae descripción de la imagen"""
        img = root.find('.//gmd:MD_ImageDescription', self.namespaces)
        if img is None:
            return None
            
        return {
            'iluminacion': self.get_element_text(img, './/gmd:illuminationElevationAngle/gco:Real'),
            'condicion': self.get_code_list_value(img, './/gmd:imagingCondition/gmd:MD_ImagingConditionCode'),
            'calidad': self.get_element_text(img, './/gmd:imageQualityCode/gco:CharacterString'),
            'porcentaje_nubes': self.get_element_text(img, './/gmd:cloudCoverPercentage/gco:Real')
        }
class MetadataValidator:
    """Clase base para validar metadatos"""
    
    def __init__(self):
        self.required_fields = {
            'metadato': {
                'codigo': True,
                'idioma': True,
                'codificacion': True,
                'contacto': {
                    'rol': True,
                    'organizacion': True,
                    'cargo': True,
                    'telefono': {
                        'numero': True,
                        'tipo': True
                    },
                    'direccion': True, 
                    'ciudad': True,
                    'pais': True,
                    'email': False,
                    'enlace': True
                },
                'fecha': {
                    'valor': True,
                    'tipo': True
                },
                'norma': {
                    'nombre': True,
                    'version': True
                },
                'perfil': {
                    'nombre': True,
                    'version': False
                },
                'ambito': True
            },
            'identificacion': {
                'titulo': True,
                'fecha': {
                    'valor': True,
                    'tipo': True
                },
                'resumen': True,
                'contacto': {
                    'rol': True,
                    'organizacion': True,
                    'cargo': True,
                    'telefono': {
                        'numero': True,
                        'tipo': True
                    },
                    'direccion': True,
                    'ciudad': True,
                    'pais': True,
                    'email': False,
                    'enlace': True
                },
                'tipo_representacion': True,
                'categoria_tema': True,
                'extension': {
                    'oeste': True,
                    'este': True, 
                    'sur': True,
                    'norte': True
                },
                'mantenimiento': {
                    'frecuencia': True
                },
                'palabras_clave': True
            }
        }
        
        self.namespaces = {
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gco': 'http://www.isotc211.org/2005/gco',
            'gts': 'http://www.isotc211.org/2005/gts', 
            'gml': 'http://www.opengis.net/gml/3.2',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }

    def validate_metadata(self, metadata: Dict) -> Tuple[List[str], List[str]]:
        """
        Valida los metadatos contra los campos requeridos
        Retorna dos listas: campos completos y campos faltantes
        """
        complete_fields = []
        missing_fields = []
        
        def check_fields(data: Dict, required: Dict, path: str = ""):
            for field, is_required in required.items():
                current_path = f"{path}.{field}" if path else field
                
                if isinstance(is_required, dict):
                    if field not in data or not isinstance(data[field], dict):
                        if self._is_any_field_required(is_required):
                            missing_fields.append(current_path)
                        continue
                    check_fields(data[field], is_required, current_path)
                else:
                    if is_required:
                        if field not in data or data[field] is None or data[field] == "":
                            missing_fields.append(current_path)
                        else:
                            complete_fields.append(current_path)
                    elif field in data and data[field]:
                        complete_fields.append(current_path)
        
        check_fields(metadata, self.required_fields)
        return complete_fields, missing_fields

    def _is_any_field_required(self, required_dict: Dict) -> bool:
        """Verifica si algún campo en el diccionario es requerido"""
        for value in required_dict.values():
            if isinstance(value, dict):
                if self._is_any_field_required(value):
                    return True
            elif value:
                return True
        return False

class VectorMetadataValidator(MetadataValidator):
    """Validador específico para metadatos de tipo vector"""
    
    def __init__(self):
        super().__init__()
        self.required_fields['vector_info'] = {
            'nivel_topologia': False,
            'objetos_geometricos': True,
            'denominador_escala': True
        }

class RasterMetadataValidator(MetadataValidator):
    """Validador específico para metadatos de tipo raster"""
    
    def __init__(self):
        super().__init__()
        self.required_fields['raster_info'] = {
            'numero_dimensiones': True,
            'dimensiones': True,
            'geometria_celda': True,
            'imagen': False
        }

def lambda_handler(event, context):
    """
    Función principal de AWS Lambda que procesa el XML desde el cuerpo del POST
    """
    try:
        # Verificar si hay contenido en el cuerpo de la solicitud
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No se encontró contenido XML en el cuerpo de la solicitud'
                })
            }
            
        # Si el contenido está en base64, decodificarlo
        if event.get('isBase64Encoded', False):
            xml_content = base64.b64decode(event['body']).decode('utf-8')
        else:
            xml_content = event['body']
            
        # Parsear el XML
        root = ET.fromstring(xml_content)
        
        # Determinar tipo de datos
        spatial_type = root.find('.//gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode', 
                               {'gmd': 'http://www.isotc211.org/2005/gmd'})
        
        if spatial_type is None:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No se pudo determinar el tipo de datos del metadato'
                })
            }
            
        type_value = spatial_type.get('codeListValue')
        
        # Seleccionar el extractor y validador apropiados
        if type_value == 'vector':
            extractor = VectorMetadataExtractor()
            validator = VectorMetadataValidator()
        elif type_value == 'grid':
            extractor = RasterMetadataExtractor()
            validator = RasterMetadataValidator()
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Tipo de datos no soportado: {type_value}'
                })
            }
            
        # Extraer y validar metadatos
        metadata = extractor.extract(root)
        complete_fields, missing_fields = validator.validate_metadata(metadata)
        
        # Calcular porcentaje de completitud
        total_fields = len(complete_fields) + len(missing_fields)
        completeness = round((len(complete_fields) / total_fields * 100), 2) if total_fields > 0 else 0
        
        # Crear diccionario de validación
        metrics_data = {
            'completeness_percentage': completeness,
            'total_fields': total_fields,
            'completed_fields_count': len(complete_fields),
            'missing_fields_count': len(missing_fields)
        }

        fields_data = {
            'complete_fields': complete_fields,
            'missing_fields': missing_fields
        }
        # Guardar XML en S3
        s3_url = save_to_s3(xml_content, type_value)
        
        # Guardar datos de validación en CSV
        validation_id, metrics_url = save_validation_metrics(metrics_data, type_value)
        fields_url = save_validation_fields(fields_data, validation_id, type_value)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'metadata': metadata,
                'validation': {
                    'metrics': metrics_data,
                    'fields': fields_data,
                    'validation_id': validation_id
                },
                'urls': {
                    'xml': s3_url,
                    'metrics_csv': metrics_url,
                    'fields_csv': fields_url
                }
            })
        }
        
    except ET.ParseError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'XML inválido',
                'details': str(e)
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")  # Log para CloudWatch
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error interno del servidor',
                'details': str(e)
            })
        }