import cv2
from flask import flash, request,  jsonify, send_from_directory
import natsort

from database import mongo_connection
import bson.json_util as json_util
from flask_pymongo import ObjectId
import shutil
from werkzeug.utils import secure_filename
import os, yaml , json
import AI.controller.projectManager as pm

db_connection = {
    "Users":mongo_connection.Users,
    "Projects":mongo_connection.Projects,
    "Annotations":mongo_connection.Annotations
}

Users = db_connection['Users']
Projects = db_connection['Projects']
Annotations = db_connection['Annotations']

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'wmv', 'flv', 'avi', 'mkv', 'webm'}



def delete_folder_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_frames(video_filepath, output_dir, Project) -> None:
        '''
        prases a video into frames and stores them as .JPG images in a directory.
        ====================================================
        Parameters:
            - video_filepath: the path to the video file.
            - output_dir: the directory path where all the frames will be stored.
        ====================================================
        Example of usage:
            > pm = ProjectManager(['cat', 'dog', 'horse'], 'animals_detection')
            > dm.extract_frames(r"path\to\video.mp4", r"path\to\images\directory")
            > print(os.listdir(r"path\to\images\directory"))
        0_animals_detection.jpg
        1_animals_detection.jpg
        2_animals_detection.jpg
        ...
        1203_animals_detection.jpg
        '''
        all_frames_paths = []
        # Open the video file
        cap = cv2.VideoCapture(video_filepath)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Initialize the frame count and loop over all frames
        total_project_images = 0
        count_init = total_project_images
        print(video_filepath, output_dir, Project['Name'],count_init)
        print(os.getcwd())
        print(os.path.exists(video_filepath))
        while True:
            # Read a frame from the video
            ret, frame = cap.read()
            # If the frame was not read successfully, break the loop
            if not ret:
                break

            # Construct the output file path and save the frame as a JPG file
            output_path = os.path.join(output_dir, f"{total_project_images}_{Project['Name']}.jpg") # EDIT projName to a class attribute
            if not os.path.exists(output_path):
                cv2.imwrite(output_path, frame)
                all_frames_paths.append(output_path)
            else:
                print(f"{output_path} already exists")

            # Increment the frame count
            total_project_images += 1
        Projects.update_one({"_id":ObjectId(Project['_id'])}, {"$set": {"Directory_of_File": output_dir, "Frames_Size": total_project_images - count_init}})
        print(f"Extracted {total_project_images - count_init} frames from {video_filepath}")
        # Release the video capture object
        cap.release()
        return (width,height)



class landingController:
    def all_projects():
        all_projects = []
        for project in Projects.find():
            all_projects.append(json.loads(json_util.dumps(project)))
        response = jsonify({"Projects":all_projects})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    def upload_video(project_name):
        Project = Projects.find_one({"Name":project_name})
        print(Project)
        # Checking whether a video was uploaded that satisfies the conditions was uploaded
        print(request.files)
        print(request.files['video'])
        if 'video' not in request.files:
            flash("No file was uploaded, Upload a video that satisfies the conditions")
            return {"Error":"No file was uploaded, Upload a video that satisfies the conditions","Project":str(ObjectId(Project['_id']))}
            # return redirect(url_for("landing.rendering"))

        # Storing the video in a temporary variable for ease of use
        file = request.files['video']

        # Checking whether a video was selected that satisfies the conditions was uploaded
        if file.filename == '':
            flash("No selected file,Upload a video that satisfies the conditions")
            return {"Error":"No selected file,Upload a video that satisfies the conditions","Project":str(ObjectId(Project['_id']))}
        if file and allowed_file(file.filename):
            os.mkdir(f'frontend/public/images/{Project["Name"]}')
            os.mkdir(f'frontend/public/images/{Project["Name"]}/video')
            file_path = os.path.join(f'frontend/public/images/{Project["Name"]}/video', secure_filename(file.filename))
            file.save(file_path)
            width,height = extract_frames(file_path,f'frontend/public/images/{Project["Name"]}', Project)
            if(not width== '1280 ' and not height=='720'):
                Projects.update_one({"_id":Project['_id']},{"$set":{"Dimensions":{"width":1280,"height":720}}})
            else:
                Projects.update_one({"_id": Project['_id']},
                                    {"$set": {"Dimensions": {"width": width, "height": height}}})
            return {"isDone":"True"}
        else:
            flash("Upload a video that satisfies the conditions")
            return {"Error":"Upload a video that satisfies the conditions","Project":str(ObjectId(Project['_id']))}
            # return redirect(url_for("landing.rendering"))

    def create_project():

        # Images (Dataset) add them to two places, public images and in AI/train_data/images
        # checking if the request sent was a post request
        if request.method == "POST":

            # Make Model and YAML files
            newProject = request.json['project']
            # Strip the name in case of whitespaces
            newProject["name"] = newProject["name"].strip()
            print(newProject['name'])
            # Strip the labels in case of whitespaces
            project_labels = [x.strip() for x in newProject['labels'].split(',')]
            index_to_labels = {i: project_labels[i] for i in range(len(project_labels))}

            print(index_to_labels)
            file_path_yaml = os.path.join('AI/yaml_files/', f'{newProject["name"]}.yaml')
            print(file_path_yaml)

            # CREATE yaml file, If no file already exits, create one and fill it with the labels
            if not os.path.exists(file_path_yaml):
                with open(file_path_yaml, 'w+') as f:
                    myDataYaml = {'path': "../AI/train_data", "train": "images/train", "val": "images/val",
                                  "names": index_to_labels.copy()}
                    yaml.dump(myDataYaml, f, sort_keys=False)

                    print(f'{file_path_yaml} created.')
            else:
                print(f'{file_path_yaml} already exists.')

            # Data from web app to add DB
            # Calculate how many frames, later compare how many written in frames size and how many files
            project_obj = {
                "Name": newProject['name'],
                "Frames_Size": '',
                "Directory_of_File": '',
                "Labels": newProject['labels'].split(','),
                "model_filepath": "AI/yolov8n.pt",
                "yaml_filepath": file_path_yaml,
                'Dimensions':{'width':0,'height':0},
                'is_training':False,
                'trained_frames':[],
                'Frames_num_to_train':50
            }
            # Add to Database
            Projects.insert_one(project_obj)
            return project_obj['Name']


    def delete_project(project_id):
        error = []
        try:
            Project = Projects.find_one({"_id": ObjectId(project_id)})
        except Exception as err:
            error.append({'error': err.__class__.__name__,'message':f"{str(err)},{error}"})
        else:
            # Remove directory and the files contained in it
            try:
                shutil.rmtree(Project['Directory_of_File'])
            except Exception as err:
                print(err)
                error.append({'error': err.__class__.__name__, 'message':f"{str(err)},{error}"})
            # Delete the directories for exported data, and delete the images and labels subfolders
            try:
                shutil.rmtree(os.getcwd()+f"/Exported_data/{Project['Name']}")
            except Exception as err:
                print(err)
                error.append({'error': err.__class__.__name__, 'message': f"{str(err)},{error}"})
            # # Delete yaml file os.getcwd()+'/'+
            try:
                os.remove(Project['yaml_filepath'])
            except Exception as err:
                print(err)
                error.append({'error': err.__class__.__name__, 'message':f"{str(err)},{error}"})
            # Delete model if the path is new
            if not Project['model_filepath'] == "AI/yolov8n.pt":
                models_filepath = os.getcwd()+'/'+ f"AI/yolov8n/runs/{Project['Name']}"
                try:
                    shutil.rmtree(models_filepath)
                except Exception as err:
                    print(err)
                    error.append({'error': err.__class__.__name__, 'message':f"{str(err)},{error}"})
            # Delete all the annotations in that project from DB and error handling because annotations are different
            try:
                Annotations.delete_many({"project_id":ObjectId(project_id)})
            except Exception as err:
                error.append({'error': err.__class__.__name__, 'message':f"{str(err)},{error}"})

            # Delete the project from DB
            Projects.delete_one({"_id": ObjectId(project_id)})
        return json.dumps({'error': error})

    def export_project(project_id):
        Project = Projects.find_one({"_id": ObjectId(project_id)})
        all_annotations = list(Annotations.find({"project_id": ObjectId(project_id),"frame": {"$in": Project['trained_frames']}},
                                                {'_id': False, 'project_id': False}))
        # Set doesn't allow duplications, give me all the frame numbers that were annotated with no duplicates
        frames_annotated = [annotation['frame'] for annotation in all_annotations]
        # after knowing the frames that were annotated, now I want a dictionary containing the frame numbers as a parent
        array_of_annotations = {}
        for frames in frames_annotated:
            array_of_annotations[frames] = []
        frame_names = []
        # the children are an array of annotations in that specific frame, parent is commented above which is frame number
        for annotation in all_annotations:
            array_of_annotations[annotation['frame']].append(annotation)

        # Check if folder for export data exist or not
        if(not os.path.exists(os.getcwd()+f"/Exported_data/{Project['Name']}")):
            # Create directories for project, then sub directories of images and labels
            os.mkdir(os.getcwd()+f"/Exported_data/{Project['Name']}")
            os.mkdir(os.getcwd()+f"/Exported_data/{Project['Name']}/images")
            os.mkdir(os.getcwd()+f"/Exported_data/{Project['Name']}/annotations")
        else:
            # Delete the directories, to empty the images and labels
            try:
                shutil.rmtree(os.getcwd()+f"/Exported_data/{Project['Name']}/images")
            except Exception as err:
                print(err)
            try:
                shutil.rmtree(os.getcwd()+f"/Exported_data/{Project['Name']}/annotations")
            except Exception as err:
                print(err)
            # Create the folders again to insert images and labels
            os.mkdir(os.getcwd()+f"/Exported_data/{Project['Name']}/images")
            os.mkdir(os.getcwd()+f"/Exported_data/{Project['Name']}/annotations")
        # Get the the image name so we can create annotation txt for it
        for frame_num in frames_annotated:
            image_name = f"{frame_num}_{Project['Name']}.jpg"
            frame_names.append(image_name)

            # export annotations
            pm.ProjectManager().create_annotations_txt(Project['yaml_filepath'], image_name,
                                                       Project['Dimensions']['width'],
                                                       Project['Dimensions']['height'], array_of_annotations[frame_num],
                                                       f'Exported_data/{Project["Name"]}/annotations')
        src_dir = Project['Directory_of_File']
        dst_dir = os.getcwd()+ f"/Exported_data/{Project['Name']}/images"
        # Only the images, copy them to the folder
        for f in frame_names:
            # Copy images to folder
            shutil.copy(src_dir + '/' + f, dst_dir)
        return {"Exported_data_location":f"Folder Created called Exported_data/{Project['Name']} and contains exported data"}
