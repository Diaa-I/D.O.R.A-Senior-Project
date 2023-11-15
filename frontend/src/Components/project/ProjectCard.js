import React, { useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './ProjectCard.css';
import axios from 'axios';

function ProjectCard({ project, setIsNewProject}) {
    const labels = project.Labels || [];

    const [showAllLabels, setShowAllLabels] = useState(false);

    const toggleLabels = () => {
        setShowAllLabels(!showAllLabels);
    };
    const buttonHandler= (event,project)=>{
        event.preventDefault()
        axios.get(`http://localhost:5000/delete_project/${project['_id']['$oid']}`)
        .then((res)=>{console.log(res.data); setIsNewProject(true)})
        .catch((err)=>{console.log(err)})
    }
    return (
        <div className="col mb-3">
            <Card style={{ width: '18rem' }}>
                <img src={`images/${project.Name}/0_${project['Name']}.jpg`} alt={project.Name} className="card-img-top" />
                <div className="card-body">
                    <h5 className="card-title">{project.Name}</h5>
                    
                    {labels.slice(0, showAllLabels ? labels.length : 5).map((label, index) => (
        <span key={index} className="circle-badge me-2">{label}</span>))}


                    {labels.length > 5 && (
                        <h6 className="more-button" onClick={toggleLabels}>
                            {showAllLabels ? 'Show less...' : 'Show more...'}
                        </h6>
                    )}

                </div>
                <Card.Footer>                    
                    <Link className="btn btn-primary" to={`/workspace/${project['_id']['$oid']}`}>Open Project</Link>
                    <button className="btn btn-danger" onClick={(e)=>buttonHandler(e,project)}>Delete Project</button>
                </Card.Footer>
            </Card>
        </div>
    );
}

export default ProjectCard;

