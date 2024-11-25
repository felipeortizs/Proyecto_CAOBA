from typing import List
import geopandas as gpd

from errors import (
    ALLOWED_EPSG_CODES,
    COULD_NOT_READ_FILE_ERROR,
    GAP_ERROR,
    INVALID_SPATIAL_REFERENCE,
    NULL_FIELD_ERROR,
    OUTSIDE_COLOMBIA,
    OVERLAP_ERROR,
    SPATIAL_REFERENCE_INCONSISTENCY,
    SUFFIX_ERROR,
)

class VectorValidator:
    def __init__(self, filepath):
        self.check_file_path(filepath)
        try:
            self.layer_names = gpd.list_layers(filepath)['name']
        except:
            raise Exception(COULD_NOT_READ_FILE_ERROR)
        self.layers = [gpd.read_file(filepath, layer=layer) for layer in self.layer_names]

    def check_file_path(self, filepath):
        allowed_suffix = ['shp', 'gdb', 'gpkg', 'kml', 'dxf']
        if len(filepath) < 3:
            raise Exception(SUFFIX_ERROR)
        suffix = filepath[-3:]
        suffix2 = filepath[-4:]
        if suffix not in allowed_suffix and suffix2 not in allowed_suffix:
            raise Exception(SUFFIX_ERROR)

    def check_null_fields(self) -> List[str]:
        errors = []
        for i, layer in enumerate(self.layers):
            layer_name = self.layer_names[i]
            for column_name, column  in layer.items():
                if self.check_null_column_value(column):
                    errors.append(NULL_FIELD_ERROR.format(
                        layer_name=layer_name,
                        column_name=column_name,
                    ))
                    break
        return errors

    def check_null_column_value(self, column) -> bool:
        for value in column:
            if self.check_for_null_value(value):
                return True
        return False

    def check_for_null_value(self, value) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            value = value.strip()
            return value != ""
        return False

    def check_inside_colombia(self) -> List[str]:
        min_longitude = -81.85
        max_longitude = -66.84
        min_latitude = -4.26
        max_latitude = 13.5

        errors = []
        for i, layer in enumerate(self.layers):
            layer_name = self.layer_names[i]

            if layer.crs.to_epsg() != 4326:
                layer = layer.to_crs(epsg=4326)

            bounds = layer.geometry.bounds

            outside = bounds[
                (bounds['minx'] < min_longitude) |
                (bounds['maxx'] > max_longitude) |
                (bounds['miny'] < min_latitude) |
                (bounds['maxy'] > max_latitude)
            ]

            if not outside.empty:
                errors.append(OUTSIDE_COLOMBIA.format(layer_name=layer_name))
        return errors

    def check_spatial_reference_consistency(self) -> List[str]:
        if len(self.layers) == 0:
            return []
        first_layer = self.layers[0]
        first_layer_name = self.layer_names[0]
        for i, layer in enumerate(self.layers):
            if first_layer.crs != layer.crs:
                layer_name = self.layer_names[i]
                return [SPATIAL_REFERENCE_INCONSISTENCY.format(
                    first_layer_name=first_layer_name,
                    layer_name=layer_name
                )]
        espg = first_layer.crs.to_epsg()
        if str(espg) not in ALLOWED_EPSG_CODES.values():
            return [INVALID_SPATIAL_REFERENCE]
        return []

    def check_overlap(self) -> List[str]:
        for layer in self.layers:
            spatial_index = layer.sindex
            for i, geom1 in enumerate(layer.geometry):
                possible_matches_index = list(spatial_index.intersection(geom1.bounds))
                possible_matches = layer.iloc[possible_matches_index]
                for j, geom2 in zip(possible_matches_index, possible_matches.geometry):
                    if i != j and geom1.intersects(geom2):
                        return [OVERLAP_ERROR]
        return []

    def check_gaps(self) -> List[str]:
        errors = []
        for i, layer in enumerate(self.layers):
            for geom in layer.geometry:
                interiors = self.extract_interiors(geom)
                if len(interiors) > 0:
                    layer_name = self.layer_names[i]
                    errors.append(GAP_ERROR.format(layer_name=layer_name))
                    break
        return errors

    def extract_interiors(self, geometry):
        if geometry.geom_type == "Polygon":
            return [list(interior.coords) for interior in geometry.interiors]

        elif geometry.geom_type == "MultiPolygon":
            interiors = []
            for polygon in geometry.geoms:
                interiors.extend([list(interior.coords) for interior in polygon.interiors])
            return interiors

        elif geometry.geom_type in ["Point", "MultiPoint", "LineString", "MultiLineString"]:
            return []
        elif geometry.geom_type == "GeometryCollection":
            interiors = []
            for geom in geometry.geoms:
                interiors.extend(self.extract_interiors(geom))
            return interiors
        else:
            return []
