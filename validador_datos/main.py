import warnings
from enums import DataTypes
from reader_validator import ReaderValidator
from pprint import pprint

warnings.filterwarnings("ignore")

filepaths = [
    (DataTypes.GDB, "/app/files/Productos_Vigentes.gdb"),
    (DataTypes.Poligon, "/app/files/Carto1000_15001000_RS_20220119.gpkg"),
    (DataTypes.Line, "/app/files/Carto1000_15001000_RS_20220119_shp"),
    (DataTypes.Point, "/app/files/KML_Samples.kml"),
    (DataTypes.DigitalTerainModel, "/app/files/Servicio-5634.tif"),
    (DataTypes.Ortoimages, "/app/files/Servicio-545.tif"),
]

for filepath in filepaths:
    try:
        rv = ReaderValidator(*filepath)
    except Exception as err:
        pprint(err)
        continue
    pprint(rv.validate())

