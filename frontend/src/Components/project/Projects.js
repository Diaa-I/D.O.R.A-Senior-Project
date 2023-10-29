// Projects.js
import React, { useState } from 'react';
import {Container , Row , Button} from 'react-bootstrap';
import SearchBar from './SearchBar';


import ProjectCard from './ProjectCard';
import ProjectModal from './ProjectModal';
import './project.css';

function Projects() {
    const [showModal, setShowModal] = useState(false);
    const [projects, setProjects] = useState([]);

    const handleCreateProject = (project) => {
        setProjects([...projects, project]);
    };

    return (
        <Container className="content mt-5">
            <div className='row'>
            <SearchBar></SearchBar>
            </div>
            
            <ProjectModal
                show={showModal}
                onHide={() => setShowModal(false)}
                onCreateProject={handleCreateProject}
            />
            <Row>{projects.map((project) => <ProjectCard key={project.name} project={project} />)}</Row>
        </Container>
    );
}

export default Projects;
