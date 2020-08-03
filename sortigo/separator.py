from PIL import Image

class Separator:
    def __init__(self, image, settings):
        self.image = Image.open(image)
        self.atlas = image.load()

        self.settings = settings

        self.init_rows(settings)
        self.shuffle_rows

    def init_rows(self, settings):
        self.rows = [[x for x in range(settings['columns'])] for y in range(settings['rows'])]
        self.settings['sector_width'] = self.settings['image_width'] / self.settings['columns']
        self.settings['sector_height'] = self.settings['image_height'] / self.settings['rows']

    from random import shuffle

    def shuffle_rows(self):
        for x in range(len(self.rows)):
            shuffle(rows[x])

    def get_located_pixel(self, sector, local_pos):
        return self.atlas[sector['x']*self.settings['sector_width'] + local_pos['x'], /
            sector['y']*self.settings['sector_height'] + local_pos['y']]
    
    def clean_all(self):
        self.image = None
        self.atlas = None
        self.settings = None

        

        



