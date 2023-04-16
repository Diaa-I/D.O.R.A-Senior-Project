import uuid
# when a button is clicked then an object is being created in the run time then sent to this class to be an object
class Annotation:
    def __init__(self, fileName, label, x_center, y_center, width, height):
        """Constructor for annotation, object for annotation"""
        self.uid = uuid.uuid4()
        self.fileName = fileName    # the image filename associated with that annotation (e.g. '125_animals.JPG')
        self.label = label          # the label name of the annotation (e.g. 'cat')
        self.x_center = x_center    # the coordinate of the center of the box on the x-axis (e.g. 245.5)
        self.y_center = y_center    # the coordinate of the center of the box on the y-axis (e.g. 180)
        self.width = width          # the width of the box
        self.height = height        # the height of the box
        self.coordinates = [self.x_center, self.y_center, self.width, self.height]

        
    def retrieve_annotation_from_db(self):
        """call the db function for that"""
        pass

    def delete_annotation(self):
        """call db class to delete annotation"""
        pass
    
    def validate_annotation(self):
        """Validate the annotation data passed"""
        pass

# Annotation class
# --------------------------------------------------------
# Variables
# Annotation dictionary (object)
# --------------------------------------------------------
# Display the frames on the user interface. (done)
#
# Display an annotation from the database (done)
#
# Make an annotation object that will be passed to the DPL layer (done)
#
# Creating a new annotation (done)
#
# Deleting an annotation from the database (done)
#
# Retrieve an annotation from the database (done)
#
# Validation (done)

