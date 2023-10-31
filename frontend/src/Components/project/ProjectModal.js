import axios from 'axios';
import React, { useState } from 'react';
import {Modal , Button ,Form} from 'react-bootstrap';


function ProjectModal({ makeNewProject,setIsNewProject }) {
    // storing the state of each field
    const [projectName, setProjectName] = useState(''); 
    const [selectedModel, setSelectedModel] = useState('model1');
    const [labels, setLabels] = useState('');
    const [datasetFile, setDatasetFile] = useState('');

    // handle opening and closing
    const [show , setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    // When the create button is clicked the values will be stored in an object
    const handleCreateProject = (e) => {
        e.preventDefault()
        let newProject = {
            name: projectName,
            model: selectedModel,
            labels: labels,
            dataset: datasetFile,
        }
        const file = e.target.video.files[0];
        const data = new FormData();
        data.append('video', e.target.video.files[0])

        makeNewProject(newProject, data);
        setIsNewProject(true)

        // Clear form fields
        setProjectName('');
        setSelectedModel('model1');
        setLabels('');
        setDatasetFile('');

        handleClose();
    };
    if(!show){
        return(
            <Button variant='primary' onClick={handleShow}>
                Create Project
            </Button>
        )
    }
    else{
    return (
        <>
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>New Project</Modal.Title>
            </Modal.Header>
            <Form onSubmit={handleCreateProject} encType='multipart/form-data'>
            <Modal.Body>
                    <Form.Group controlId="projectName">
                        <Form.Label>Project Name:</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter project name"
                            value={projectName}
                            onChange={(e) => setProjectName(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group controlId="modelSelect">
                        <Form.Label>Choose Model:</Form.Label>
                        <Form.Control
                            as="select"
                            value={selectedModel}
                            onChange={(e) => setSelectedModel(e.target.value)}
                        >
                            <option value="model1">Model 1</option>
                            <option value="model2">Model 2</option>
                            <option value="model3">Model 3</option>
                        </Form.Control>
                    </Form.Group>
                    <Form.Group controlId="labels">
                        <Form.Label>Labels (separated by comma):</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter labels"
                            value={labels}
                            onChange={(e) => setLabels(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group controlId="datasetUpload">
                        <Form.Label>Upload Dataset:</Form.Label>
                        <Form.Control
                            type="file"
                            value={datasetFile}
                            name='video'
                            onChange={(e) => setDatasetFile(e.target.value)}
                        />
                    </Form.Group>
                    </Modal.Body>
             <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
                {/* onClick={handleCreateProject}    */}
                <Button variant="primary" type='submit'>
                    Create
                </Button>

            </Modal.Footer>
            </Form>
        </Modal>
        </>

    );
}
}

export default ProjectModal;
