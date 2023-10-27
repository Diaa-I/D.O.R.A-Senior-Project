import controller.modelController as mc
import controller.projectManager as pm

myPM = pm.ProjectManager(['glass', 'metal', 'paper'], 
                          projectName='trash_detection')

myPM.createYaml(at="sandbox")
myMC = mc.ModelController()

myMC.trainModel(yamlFilepath="sandbox/trash_detection.yaml", 
                pretrainedWeights="yolov5m/yolov5n.pt",
                imgTrainSize=320,
                batch_size=8)

# myMC.makeInference()