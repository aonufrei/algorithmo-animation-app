from PIL import Image

class Separator:
    def __init__(self, image):
        self.image = Image.open(image)
        self.image.show()
        
        



