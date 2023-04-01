
class File:
    def __init__(self, file):
        self.file = file
    def cut_into_frames(self):
        """Cut the frames"""
        pass
    def save_file_to_db(self):
        """Call to DB to save the file"""
        pass
    def save_frame_to_db(self):
        """Call to DB to save the frame"""
        pass
    def update_file_to_db(self):
        """Update the files, because of the annotations"""
        pass
    def delete_file(self):
        """Delete the file from db, by calling function in db class"""
        pass
    def retrieve_frame_annotation(self):
        """Retrieve a frame with all it's annotation"""
        pass
    def validate_video(self):
        """Unsure what needs to be validated"""
        pass

# File class
# --------------------------------------------------------
# Upload video (done)
#
# Cutting into frames (done)
#
# Display a frame with all it is annotations (from db)
#
# Make a file that will be passed to the DPL layer (done)
#
# Save frames into disk (done)
#
# Inserting a video into the database (done)
#
# Updating a video in the database (done)
#
# Deleting a video from the database (done)
#
# Retrieve a frame with all it is annotations (done)
#
# Validation