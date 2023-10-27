import controller as con
import os

dm = con.projectManager.ProjectManager(['cat', 'dog', 'lion'], 'animals_detection')
dm.extract_frames(video_filepath=r".\sandbox\sample.mp4", output_dir=r".\sandbox\data")

# batch = dm.retrieveNextBatch()
# for i in range(2):
#     print(f"BATCH NO. {dm.imageRetrievalIndex}:\n {batch}", end="\n\n")
#     batch = dm.retrieveNextBatch()

print(dm.retrieve_previous_batch(starting_from=45), end="\n\n")
print(dm.retrieve_previous_batch(), end="\n\n")
print(f"imageRetrievalIndex={dm.image_retrieval_index} \ntotalProjectImages={dm.total_project_images}", end="\n\n")

# remove everything
for file in os.listdir("./sandbox/data"):
    os.remove(os.path.join(r".\sandbox\data", file))
print("ALL FILES REMOVED")