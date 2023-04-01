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


# Key Name	Definition	Parent Key
# annotations	List of annotations	N/A
# id	Annotations ID	annotations
# datasetId	Dataset ID	annotations
# type	Annotation type	annotations
# label	The annotation's label/class	annotations
# attributes
# Annotation 1.0 format – list of annotation attributes
# Annotation 2.0 format – dictionary of annotation attributes
# annotations
# metadata	This key holds all of the annotation information	annotations
# system	This key holds all of the annotation system information	metadata
# status	QA status for annotation	system
# startTime	The start time of the annotation in video items	system
# endTime	The end time of the annotation in video items	system
# frame	The first frame of the annotation in video items	system
# endFrame	The end frame of the annotation in video items	system
# snapshots_	Snapshot information Relevant for video annotation	system
# fixed	Frame that was changed by a user if true or interpulated if false	snapshots_
# type	Snapshot stype	snapshots_
# frame	Snapshot frame number	snapshots_
# objectVisible	Status of annotation, true = visible and false = hidden	snapshots_
# data	Coordinates of the annotation in each snapshot	snapshots_
# label	Snapshot label	snapshots_
# attributes	Snapshots attributes	snapshots_
# parentId	The ID of parent annotation	system
# objectId	The annotation's Object ID	system
# automated	If the frame is automated	system
# isOpen	For Polygon and Polyline annotation, False = Closed shape (Polygon), True = Open shape (Polyline)	system
# system	True - the system created this specific annotation False - annotation was created on a different way	system
# description	Annotation text description	system
# openAnnotationVersion	product version	system
# user	Metadata that can be added by user via SDK	annotations
# creator	Annotation creator	annotations
# createdAt	Annotation creation date and time	annotations
# updatedBy	Annotation edits by user name	annotations
# updatedAt	Annotation edits date and time	annotations
# itemId	Item/image ID	annotations
# taskId	Task ID of the task the annotation was made in	system
# assignmentId	Assignment ID of the assignment the annotation was made in	system
# isOnlyLocal	A field used in the UI to determine if the annotation is ready to be saved or not (False – ready to be saved)	system
# url	API url for annotation	annotations
# item	API url for image item	annotations
# dataset	API url for dataset	system
# hash	Used to map the item’s data to a string of arbitrary size	system
# coordinates	Annotation position coordinates	system
# _id	Item/image ID	N/A
# filename	Item/image path in the dataset	N/A