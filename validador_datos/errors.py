SUFFIX_ERROR = (
    "El archivo no se pudo leer porque no es de los tipos acceptados para vector." \
    "Los tipos aceptados para vector son shp, gdb, gpkg, kml, y dxf."
)
COULD_NOT_READ_FILE_ERROR = "No se pudo leer el archivo"
NO_MATCHING_TYPE = "El tipo de archivo no coincide con los especificados"
NULL_FIELD_ERROR = "La capa {layer_name} en la columna {column_name} tiene un valor nulo"
SPATIAL_REFERENCE_INCONSISTENCY = (
    "Existe una incosistencia entre el punto de origen de de la capa {first_layer_name} y {layer_name}"
)
OUTSIDE_COLOMBIA = "La capa '{layer_name}' tiene geometrías fuera de Colombia."
INVALID_SPATIAL_REFERENCE = (
    "El punto de origen del archivo no se es validos." \
    "Los puntos de origen validos son estan en esta url https://origen.igac.gov.co/herramientas.html."
)
OVERLAP_ERROR = "Superposition en el archivo"
GAP_ERROR = "Hueco en la capa {layer_name}"
OUTSIDE_COLOMBIA_TIFF = "El raster esta fuera de Colombia"
BANDS_ERROR = "La Ortoimagen no tiene las tres minimas bandas rojo, azul y verde"
RADIOMETRIC_ERROR = "La Ortoimagen no tiene la minima resolución de radiometria"

ALLOWED_EPSG_CODES = {
    "Magna Origen Único": "9377",
    "WGS 84": "4326",
    "WGS84 Web Mercator": "3857",
    "MAGNA-SIRGAS": "4686",
    "MAGNA-SIRGAS / Colombia Far West zone": "3114",
    "MAGNA-SIRGAS / Colombia West zone": "3115",
    "MAGNA-SIRGAS / Colombia Bogota zone": "3116",
    "MAGNA-SIRGAS / Colombia East Central zone": "3117",
    "MAGNA-SIRGAS / Colombia East zone": "3118",
    "Bogota 1975 / Colombia East": "21894",
    "Bogota 1975 / Colombia West zone": "21896",
    "Bogota 1975 / Colombia Bogota zone": "21897",
    "Bogota 1975 / Colombia East Central zone": "21898",
    "Bogota 1975 / Colombia East zone": "21899",
    "MAGNA-SIRGAS / Arauca urban grid": "6244",
    "MAGNA-SIRGAS / Armenia urban grid": "6245",
    "MAGNA-SIRGAS / Barranquilla urban grid": "6246",
    "MAGNA-SIRGAS / Bogota urban grid": "6247",
    "MAGNA-SIRGAS / Bucaramanga urban grid": "6248",
    "MAGNA-SIRGAS / Cali urban grid": "6249",
    "MAGNA-SIRGAS / Cartagena urban grid": "6250",
    "MAGNA-SIRGAS / Cucuta urban grid": "6251",
    "MAGNA-SIRGAS / Florencia urban grid": "6252",
    "MAGNA-SIRGAS / Ibague urban grid": "6253",
    "MAGNA-SIRGAS / Inirida urban grid": "6254",
    "MAGNA-SIRGAS / Leticia urban grid": "6255",
    "MAGNA-SIRGAS / Manizales urban grid": "6256",
    "MAGNA-SIRGAS / Medellin urban grid": "6257",
    "MAGNA-SIRGAS / Mitu urban grid": "6258",
    "MAGNA-SIRGAS / Mocoa urban grid": "6259",
    "MAGNA-SIRGAS / Monteria urban grid": "6260",
    "MAGNA-SIRGAS / Neiva urban grid": "6261",
    "MAGNA-SIRGAS / Pasto urban grid": "6262",
    "MAGNA-SIRGAS / Pereira urban grid": "6263",
    "MAGNA-SIRGAS / Popayan urban grid": "6264",
    "MAGNA-SIRGAS / Puerto Carreno urban grid": "6265",
    "MAGNA-SIRGAS / Quibdo urban grid": "6266",
    "MAGNA-SIRGAS / Riohacha urban grid": "6267",
    "MAGNA-SIRGAS / San Andres urban grid": "6268",
    "MAGNA-SIRGAS / San Jose del Guaviare urban grid": "6269",
    "MAGNA-SIRGAS / Santa Marta urban grid": "6270",
    "MAGNA-SIRGAS / Sucre urban grid": "6271",
    "MAGNA-SIRGAS / Tunja urban grid": "6272",
    "MAGNA-SIRGAS / Valledupar urban grid": "6273",
    "MAGNA-SIRGAS / Villavicencio urban grid": "6274",
    "MAGNA-SIRGAS / Yopal urban grid": "6275",
    "WGS 84 / UTM zone 17N": "32617",
    "WGS 84 / UTM zone 18N": "32618",
    "WGS 84 / UTM zone 19N": "32619",
    "WGS 84 / UTM zone 17S": "32717",
    "WGS 84 / UTM zone 18S": "32718",
    "WGS 84 / UTM zone 19S": "32719"
}
