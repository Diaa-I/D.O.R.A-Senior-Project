// import 'bootstrap/dist/css/bootstrap.css';
function Project_Modal(){
    return(
        <>
        <div class="container mt-5">
        <div id="project-modal" class="modal fade" tabindex="-1" aria-labelledby="modal-title" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modal-title">New Project</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <div class="form-group">
                                <label for="projectName">Project Name:</label>
                                <input type="text" class="form-control" id="projectName" name="projectName" />
                            </div>
                            <div class="form-group">
                                <label for="modelSelect">Choose Model:</label>
                                <select class="form-control" id="modelSelect" name="modelSelect">
                                    <option value="model1">Model 1</option>
                                    <option value="model2">Model 2</option>
                                    <option value="model3">Model 3</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="labels">Labels (separated by comma):</label>
                                <input type="text" class="form-control" id="labels" name="labels" />
                            </div>
                            <div class="form-group">
                                <label for="datasetUpload">Upload Dataset:</label>
                                <input type="file" class="form-control-file" id="datasetUpload" name="datasetUpload" />
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id="create-project-button" class="btn btn-primary">Create</button>
                    </div>

                    </div>

                </div>
            </div>
            
    </div> 
        </>
    )
}
export default Project_Modal;