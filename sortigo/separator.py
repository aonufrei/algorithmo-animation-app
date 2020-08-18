from PIL import Image

from . exceptions import BadSettingsTypeException
from . exceptions import NullSettingsException
#Settings has
#image_width
#image_height
#columns
#rows

class Separator:

    def __init__(self, image: str, settings: dict):
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
        
        self.image_width, self.image_height = self.image.size
        
        self.segment_width = self.image_width // self.columns
        self.segment_height = self.image_height // self.rows
        
    def create_segment(self, x: int, y: int):
        #print("{} {}".format(x, y))
        segment_x_edge = (x+1) * self.segment_width  if x != self.columns-1 else self.image_width  
        segment_y_edge = (y+1) * self.segment_height if y != self.rows-1    else self.image_height

        return [x, (x*self.segment_width, y*self.segment_height, segment_x_edge, segment_y_edge)]

    def init_row_arrays(self):
        self.row_arrays = [[self.create_segment(x, y) for x in range(self.columns)] for y in range(self.rows)]
        #print(self.row_arrays)

    def get_segment(self, x: int, y: int):
        #print(self.row_arrays[y][x])

        segment = self.row_arrays[y][x][1]
        #print(segment)
        return dict(region=self.atlas.crop(segment), pos_size=segment)

    def shuffle_row_arrays(self): 
        from random import shuffle
        for x in range(self.rows):
            shuffle(self.row_arrays[x])
        #print(self.row_arrays)

    
    def check_int_variable_type(self, variable):
        if type(variable) != int:
            raise BadSettingsTypeException("The variable must be of type int, but it is of type" + str(type(variable)))
    
    def check_if_none(self, variable):
        if variable == None:
            raise NullSettingsException("This variable cannot be Null")

        

        



