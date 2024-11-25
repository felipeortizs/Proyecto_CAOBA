from osgeo import gdal, osr, ogr
from errors import (
    ALLOWED_EPSG_CODES,
    BANDS_ERROR,
    COULD_NOT_READ_FILE_ERROR,
    INVALID_SPATIAL_REFERENCE,
    OUTSIDE_COLOMBIA_TIFF,
    RADIOMETRIC_ERROR,
    SUFFIX_ERROR,
)

class TIFFValidator:
    def __init__(self, filepath):
        self.check_file_path(filepath)
        self.dataset = gdal.Open(filepath, gdal.GA_ReadOnly)
        if not self.dataset:
            raise Exception(COULD_NOT_READ_FILE_ERROR)

    def check_file_path(self, filepath):
        if len(filepath) < 3:
            raise Exception(SUFFIX_ERROR)
        suffix = filepath[-3:]
        if suffix == 'tif':
            return
        if suffix == 'geotif':
            return
        raise Exception(SUFFIX_ERROR)

    def check_if_inside_colombia(self):
        geotransform = self.dataset.GetGeoTransform()
        projection = self.dataset.GetProjection()
        if not geotransform or not projection:
            return False

        srs_dataset = osr.SpatialReference()
        srs_dataset.ImportFromWkt(projection)

        srs_wgs84 = osr.SpatialReference()
        srs_wgs84.ImportFromEPSG(4326)

        transform = osr.CoordinateTransformation(srs_dataset, srs_wgs84)

        width = self.dataset.RasterXSize
        height = self.dataset.RasterYSize

        x_min = geotransform[0]
        y_max = geotransform[3]
        x_max = x_min + geotransform[1] * width
        y_min = y_max + geotransform[5] * height

        corner_points = [
            (x_min, y_max),
            (x_max, y_max),
            (x_max, y_min),
            (x_min, y_min),
        ]

        corner_points_wgs84 = []
        for x, y in corner_points:
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(x, y)
            point.Transform(transform)
            lon, lat = point.GetX(), point.GetY()
            corner_points_wgs84.append((lon, lat))

        min_lon = -4.0
        max_lon = 15.0
        min_lat = -81.0
        max_lat = -66.0

        for lon, lat in corner_points_wgs84:
            if not (min_lon <= lon and lon <= max_lon and min_lat <= lat and lat <= max_lat):
                return [OUTSIDE_COLOMBIA_TIFF]

        return [] 

    def check_spatial_reference_consistency(self):
        projection = self.dataset.GetProjection()
        srs = osr.SpatialReference()
        srs.ImportFromWkt(projection)
        if projection is None:
            return [INVALID_SPATIAL_REFERENCE]
        authority_name = srs.GetAuthorityName('PROJCS')
        authority_code = srs.GetAuthorityCode('PROJCS')
        if authority_name is None or authority_code is None:
            return [INVALID_SPATIAL_REFERENCE]
        if not (authority_name == 'EPSG' and authority_code in ALLOWED_EPSG_CODES.values()):
            return [INVALID_SPATIAL_REFERENCE]
        return []

    def check_bands(self):
        band_count = self.dataset.RasterCount
        if band_count < 3:
            return [BANDS_ERROR]
        band_color_set = set()
        for band_index in range(1, band_count + 1):
            band = self.dataset.GetRasterBand(band_index)
            color_interp = band.GetColorInterpretation()
            band_color_set.add(color_interp)
        if gdal.GCI_RedBand not in band_color_set:
            return [BANDS_ERROR]
        if gdal.GCI_BlueBand not in band_color_set:
            return [BANDS_ERROR]
        if gdal.GCI_GreenBand not in band_color_set:
            return [BANDS_ERROR]
        return []

    def check_radiometric_resolution(self):
        for band_index in range(1, self.dataset.RasterCount + 1):
            band = self.dataset.GetRasterBand(band_index)
            data_type = band.DataType
            bits_per_pixel = gdal.GetDataTypeSize(data_type)
            if bits_per_pixel < 8:
                return [RADIOMETRIC_ERROR]
        return []
