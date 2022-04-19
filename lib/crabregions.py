from regions import (read_ds9, write_ds9, ds9_objects_to_string, 
                     Region, RectangleSkyRegion, PixelRegion, PixCoord)
try:
    from regions import Regions
    my_ds9_parser = Regions.parse
except:
    from regions import DS9Parser, ShapeList, Shape
    my_ds9_parser = lambda x: [t.to_region() for t in DS9Parser(x).shapes]
    #DS9Parser deprecated, use Regions.parse(regions_str, format='ds9')


