// Projects.js
import React, { useEffect, useState } from 'react';
import { Container, Row, Button, Col } from 'react-bootstrap';
import SearchBar from './SearchBar';
import ProjectCard from './ProjectCard';
import ProjectModal from './ProjectModal';
import LoadingModal from '../workspace/LoadingModal';
import './project.css';
import axios from 'axios';

function Projects(props) {
    const [showModal, setShowModal] = useState(false);
    const [projects, setProjects] = useState([]);
    const [isNewProject, setIsNewProject] = useState(true);
    const [isLoading,setIsLoading] = useState(false)
    const handleClose = () => {setShowModal(false);}
    const handleShow = () => {setShowModal(true);}

    useEffect(() => {
        if (isNewProject) {
            axios.get("http://localhost:5000/all_projects")
                .then((res) => {
                    setProjects(res.data['Projects'])
                    setIsNewProject(false)
                })
                .catch((err) => { console.log(err) })

        }
    }, [isNewProject]);

    const makeNewProject = (project,data)=>{        
        setIsLoading(true)
        axios.post('http://localhost:5000/create_project',{"project":project})
            .then((res)=>{
            axios.post(`http://localhost:5000/upload_video/${res.data}`,data).then((res)=>{
            setIsNewProject(true);
            setIsLoading(false) 
            }).catch((err)=>console.log(err))
            })
            .catch((err)=>console.log(err))
    }

    return (
        <Container className="content mt-5">
            <LoadingModal isLoading={isLoading}/>
            <div className='row'>
            <Button variant='primary' onClick={handleShow}>Create Project</Button>
            <SearchBar projects={projects}></SearchBar>
            </div>
            <ProjectModal
                show={showModal}
                onHide={handleClose}
                makeNewProject={makeNewProject}
            />
            {console.log(projects)}
            <Row>
                {projects.map((project) => <ProjectCard   key={project.name} project={project} setIsNewProject={setIsNewProject} />)}
            </Row>
        </Container>
    );
}

export default Projects;
