import axios from 'axios';
import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

function ProjectModal({ makeNewProject,onHide,show }) {
    // storing the state of each field
    const [projectName, setProjectName] = useState(''); 
    const [labels, setLabels] = useState('');
    const [datasetFile, setDatasetFile] = useState('');

    const handleCreateProject = (e) => {
        e.preventDefault();
        const cleanedLabels = labels.replace(/\s/g, '');
        console.log(e.target.value)
        let newProject = {
            name: projectName,
            labels: cleanedLabels,
            dataset: datasetFile,
        };
        const file = e.target.video.files[0];
        const data = new FormData();
        data.append('video', e.target.video.files[0]);
        // Related to modal
        setProjectName('');
        setLabels('');
        setDatasetFile('');
        onHide();
        // related to project
        makeNewProject(newProject, data);
    };

    console.log(show)
    return (
        <>
        {console.log(show)}
        {console.log(onHide)}
            <Modal show={show} onHide={onHide} style={{ backgroundColor: 'rgba(255, 255, 255, 0)' }}>
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
                        <Button variant="secondary" onClick={onHide}>
                            Close
                        </Button>
                        <Button variant="primary" type='submit'>
                            Create
                        </Button>
                    </Modal.Footer>
                </Form>
            </Modal>
        </>
    );
}

export default ProjectModal;
