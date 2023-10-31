// Projects.js
import React, { useEffect,useState } from 'react';
import {Container , Row , Button} from 'react-bootstrap';
import SearchBar from './SearchBar';


import ProjectCard from './ProjectCard';
import ProjectModal from './ProjectModal';
import './project.css';
import axios from 'axios';
function Projects(props) {
    const [showModal, setShowModal] = useState(false);
    const [projects, setProjects] = useState([]);
    const [isNewProject,setIsNewProject] = useState(true)
    useEffect(()=>{
        if(isNewProject){
            
        axios.get("http://localhost:5000/all_projects")
        .then((res)=>{
            console.log(res.data)
            setProjects(res.data['Projects'])
            setIsNewProject(false)
        })
        .catch((err)=>{console.log(err)})
        
    }
    },[isNewProject])

    const makeNewProject = (project,data)=>{
        axios.post('http://localhost:5000/create_project',{"project":project})
            .then((res)=>{
                axios.post(`http://localhost:5000/upload_video/${res.data}`,data).then((res)=>{
            console.log(res)
            }).catch((err)=>console.log(err))
            })
            .catch((err)=>console.log(err))
        
        
    }
    return (
        <Container className="content mt-5">
            <div className='row'>
            <SearchBar></SearchBar>
            </div>
            
            <ProjectModal
                show={showModal}
                onHide={() => setShowModal(false)}
                // onCreateProject={handleCreateProject}
                setProjects={setProjects}
                makeNewProject={makeNewProject}
                setIsNewProject={setIsNewProject}
            />
            <Row>{projects.map((project) => <ProjectCard key={project.name} project={project} />)}</Row>
        </Container>
    );
}

export default Projects;
