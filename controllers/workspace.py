import os
from flask import Flask,flash,render_template,redirect,request,url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from database import mongo_connection
from bson.objectid import ObjectId
# from AI.controller.dataManager import ProjectManager
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'wmv', 'flv', 'avi', 'mkv', 'webm'}

db_connection = {
    "Users":mongo_connection.Users,
    "Projects":mongo_connection.Projects
}

Users = db_connection['Users']
Projects = db_connection['Projects']
print(Users.find_one())
print(Projects.find_one())


def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# To be changed to WorkspaceController
class workspaceController:
    project_name = ""
    def get_labels():
        # function to get labels that were entered by the user
        labels = []
        # Labels are stored in a file, once the form is submitted in the landing page
        with open('uploads\\files\\labels.txt','r') as label_file:
            labels.append(label_file.readline().strip().split(","))
        # the labels are returned to be used on the front end
        response = jsonify({"labels":labels[0]})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    def get_project_information():
        Project = Projects.find_one({})
        print(Project)
        response = jsonify({"Project_Name": Project['Name'], "Frames": Project['Frames_Size']})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Headers", "X-Requested-With");
        print(response)
        return response

    def get_next_frames():
    #     Function to get the Next set of frames (to be annotated)
    #     Using the project_id we retieve it from the database, Directory_of_File\Frame_number loop * numberOfRetrievals
    #
        pass
    def get_old_frames():
    #     Function to get the previous set of frames or frame (That were already annotated even if skipped)
        pass
    # print(app.Project.find_one_or_404({"_id":"651aed7e0fa9d4b9db48be1b"}))


    def workspace():
        # checking if the request sent was a post request
        if request.method == "POST":
            # Checking whether a video was uploaded that satisfies the conditions was uploaded
            if 'video' not in request.files:
                flash("No file was uploaded, Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))

            # Storing the video in a temporary variable for ease of use
            file = request.files['video']

            # Checking whether a video was selected that satisfies the conditions was uploaded
            if file.filename == '':
                flash("No selected file,Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))


            if file and allowed_file(file.filename):
                file_path = os.path.join('uploads/files', secure_filename(file.filename))
                file.save(file_path)

                project_name = request.form['project_name']
                # labels = request.form['labels'].split(",")
                # file_path = file_path
                # DM_obj = DataManager('',project_name)

                path = os.getcwd()
                # DM_obj.extractFrames(file_path,path+'/AI/train_data/images')

                # here is where the labels are stored in a file
                with open("./uploads/files/labels.txt",'w+') as label_file:
                    label_file.writelines(request.form['labels'])
                # returning the SPA page
                return send_from_directory(path+'/frontend/build/',"index.html")
                # return render_template("/views/workspace.html", filename=file.filename, labels=labels)
            else:
                flash("Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))

    def retrieve_next_batch(self, starting_from=None, retrieval_size=10):
        '''
        returns retrieval_size number of images filepaths in batches every time it's called. Starts from 0 index and moves retrieval_size.
        retrieval_size is set to 10 by default.
        ====================================================
        Parameters:
            - retrieval_size: the number of filepaths to be returned in each batch.
        ====================================================
        returns: list of relative filepaths to 'outputDir' of all the files stored in 'outputDir'. Returns empty list once all filepaths
        have been returned.
        ====================================================
        Example of usage:
            > dm = ProjectManager(['cat', 'dog', 'lion'], 'animals_detection')
            > dm.extractFrames(videoFilepath=r".\dir\Vid.mp4", outputDir=r".\data")
            > dm.retrieve_next_batch()
        .\\data\\0_animals_detection.jpg
        .\\data\\1_animals_detection.jpg
        .\\data\\2_animals_detection.jpg
        ...
        .\\data\\9_animals_detection.jpg
            > dm.retrieve_next_batch()
        .\\data\\10_animals_detection.jpg
        .\\data\\11_animals_detection.jpg
        .\\data\\12_animals_detection.jpg
        ...
        .\\data\\19_animals_detection.jpg
        
        '''
        # instance variables that are unimplemented:
        #   - self.total_project_images -> the total number of images stored in the list.
        #   - self.all_stored_filepaths -> the list which contains all the filepaths of the images.
        #   - self.image_retrieval_index -> used as a global pointer to where to start retrieving in the list.

        self.image_retrieval_index = starting_from if starting_from is not None else self.image_retrieval_index
        start = self.image_retrieval_index
        end = self.image_retrieval_index + retrieval_size

        if start < self.total_project_images - 1:
            if end < self.total_project_images - 1:
                self.image_retrieval_index = end
                batch_filepaths_json = jsonify({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": self.all_stored_filepaths[start:end]
                })
                return batch_filepaths_json
            else:
                end = self.total_project_images - 1
                self.image_retrieval_index = end
                batch_filepaths_json = jsonify({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": self.all_stored_filepaths[start:end]
                })
                return batch_filepaths_json
        else:
            batch_filepaths_json = jsonify({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": []
                })
            return batch_filepaths_json

    def retrieve_previous_batch(self, starting_from=None, retrieval_size=10):
        '''
        returns the previous retrieval_size number of images filepaths in batches every time it's called. Starts from 'starting_from' as an index.
        ====================================================
        Parameters:
            - retrieval_size: the number of filepaths to be returned in each batch.
            - starting_from: the index at which the previous batch will be retrieved. Defaults to the global imageRetrievalIndex pointer.
        ====================================================
        returns: list of relative filepaths to 'outputDir' of all the files stored in 'outputDir'. Returns empty list once all filepaths
        have been returned.
        ====================================================
        Example of usage:
            > dm = ProjectManager(['cat', 'dog', 'lion'], 'animals_detection')
            > dm.extractFrames(videoFilepath=r".\dir\Vid.mp4", outputDir=r".\data")
            > dm.retrieve_previous_batch(starting_from=100, retrieval_size=2)
        .\\data\\99_animals_detection.jpg
        .\\data\\100_animals_detection.jpg
            > dm.retrieve_previous_batch()
        .\\data\\97_animals_detection.jpg
        .\\data\\98_animals_detection.jpg
        '''
        # instance variables that are unimplemented:
        #   - self.total_project_images -> the total number of images stored in the list.
        #   - self.all_stored_filepaths -> the list which contains all the filepaths of the images.
        #   - self.image_retrieval_index -> used as a global pointer to where to start retrieving in the list.

        self.image_retrieval_index = starting_from if starting_from is not None else self.image_retrieval_index
        start = self.image_retrieval_index
        end = start - retrieval_size

        if start > 0 and start < self.total_project_images:
            if end > -1:
                self.image_retrieval_index = end
                batch_filepaths_json = jsonify({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": self.all_stored_filepaths[end+1:start+1]
                })
                return batch_filepaths_json
            else:
                batch_filepaths_json = jsonify({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": self.all_stored_filepaths[0:start]
                })
                return batch_filepaths_json
        else:
            batch_filepaths_json = jsonify({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": []
            })
            return batch_filepaths_json