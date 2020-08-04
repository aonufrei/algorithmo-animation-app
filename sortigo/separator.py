from PIL import Image

from . exceptions import BadSettingsTypeException
from . exceptions import NullSettingsException
#Settings has
#image_width
#image_height
#columns
#rows

class Separator:
    def __init__(self, image:str, settings:dict):
        self.image = Image.open(image)
        self.atlas = self.image.convert('RGBA')
        
        self.settings = settings

        self.init_settings(settings)
        self.init_row_arrays()
        self.shuffle_row_arrays()


    def init_settings(self, settings):
        self.columns = settings['columns']
        self.check_int_variable_type(self.columns)
        self.check_if_none(self.columns)

        self.rows = settings['rows']
        self.check_int_variable_type(self.rows)
        self.check_if_none(self.rows)
        
        self.image_width = settings['image_width']
        self.check_int_variable_type(self.image_width)
        self.check_if_none(self.image_width)

        self.image_height = settings['image_height']
        self.check_int_variable_type(self.image_height)
        self.check_if_none(self.image_height)
        
        self.sector_width = self.image_width // self.columns
        self.sector_height = self.image_height // self.rows
        
    def init_row_arrays(self):
        self.row_arrays = [[x for x in range(self.columns)] for y in range(self.rows)]


    def detect_sector(self, pos_x:int, pos_y:int):
        sector_x = pos_x//self.sector_width
        sector_y = pos_y//self.sector_height
        return dict(x=sector_x, y=sector_y)

    def get_local_coords(self, pos_x:int, pos_y:int):
        sector = self.detect_sector(pos_x, pos_y)
        local_x = pos_x - sector['x'] * self.sector_width
        local_y = pos_y - sector['y'] * self.sector_height
        return dict(x=local_x, y=local_y)

    def shuffle_row_arrays(self): 
        from random import shuffle
        for x in range(len(self.row_arrays)):
            shuffle(self.row_arrays[x])

    def get_selected_pixel(self, sector:dict, local_pos:dict):
        selected_x = sector['x']*self.sector_width + local_pos['x']
        selected_y = sector['y']*self.sector_height + local_pos['y']
    #    print("{0} {1}".format(selected_x, selected_y))
        return self.atlas.getpixel( (selected_x, selected_y) )
    
    def check_int_variable_type(self, variable):
        if type(variable) != int:
            raise BadSettingsTypeException("The variable must be of type int, but it is of type" + str(type(variable)))
    
    def check_if_none(self, variable):
        if variable == None:
            raise NullSettingsException("This variable cannot be Null")

    def clean_all(self):
        self.image = None
        self.atlas = None
        self.settings = None

        

        



