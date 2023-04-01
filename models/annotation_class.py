import uuid
# when a button is clicked then an object is being created in the run time then sent to this class to be an object
class Annotation:
    def __init__(self, user, type_annotation, label, coordinates):
        """Constructor for annotation, object for annotation"""
        self.uid = uuid.uuid4()
        self.type = type_annotation
        self.label = label
        self.coordinates = coordinates
        self.user = user
        pass
    def retrieve_annotation_from_db(self):
        """call the db function for that"""
        pass
    def save_to_db(self):
        """call db class to save annotation"""
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

