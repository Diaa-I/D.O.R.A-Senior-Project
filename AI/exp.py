import controller as con
import os

dm = con.dataManager.ProjectManager(['cat', 'dog', 'lion'], 'animals_detection')
dm.extractFrames(videoFilepath=r".\sandbox\sample.mp4", outputDir=r".\sandbox\data")

batch = dm.retrieveNextBatch()
while len(batch) != 0:
    print(f"BATCH NO. {dm.imageRetrievalIndex}:\n {batch}", end="\n\n")
    batch = dm.retrieveNextBatch()

print(f"imageRetrievalIndex={dm.imageRetrievalIndex} \ntotalProjectImages={dm.totalProjectImages}", end="\n\n")

# remove everything
for file in os.listdir("./sandbox/data"):
    os.remove(os.path.join(r".\sandbox\data", file))
print("ALL FILES REMOVED")