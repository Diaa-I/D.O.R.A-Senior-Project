import controller as con
import os

pm = con.projectManager.ProjectManager(['plastic', 'metal', 'paper'], project_name="trash_detection")

pm.create_annotations_txt("frame_00423", 400, 600, [{'label': 'plastic', 'x_center':80, 'y_center': 234, 'width': 30, 'height':80}, {'label': 'plastic', 'x_center':80, 'y_center': 234, 'width': 30, 'height':80}], "./sandbox")