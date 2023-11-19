import React, { useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './ProjectCard.css';
import axios from 'axios';

function ProjectCard({ project,frameSize , trainedFrames, setIsNewProject,setIsLoading}) {
    const labels = project.Labels || [];
    const progress = (trainedFrames / frameSize) * 100;

    const [showAllLabels, setShowAllLabels] = useState(false);

    const toggleLabels = () => {
        setShowAllLabels(!showAllLabels);
    };
    const buttonHandler= (event,project)=>{
        event.preventDefault()
        setIsLoading(true)
        axios.get(`http://localhost:5000/delete_project/${project['_id']['$oid']}`)
        .then((res)=>{console.log(res.data);setIsLoading(false); setIsNewProject(true);})
        .catch((err)=>{console.log(err);setIsLoading(false);})
    }
    return (
        <div className="col mb-3">
            <Card style={{ width: '18rem' }}>
                <img src={`images/${project.Name}/0_${project['Name']}.jpg`} alt={project.Name} className="card-img-top" />
                <div className="card-body">
                    <h5 className="card-title">{project.Name}</h5>
                    
                    {labels.slice(0, showAllLabels ? labels.length : 5).map((label, index) => (
        <span key={index} className="badge rounded-pill text-bg-primary me-2">{label}</span>))}


                    {labels.length > 5 && (
                        <h6 className="more-button text-end" onClick={toggleLabels} style={{ fontSize: '10px', color: 'grey'}}>
                            {showAllLabels ? 'Show less...' : 'Show more...'}
                        </h6>
                    )}

                </div>
                <div className='d-inline-flex gap-2 justify-content-end me-3 mb-2'>
                    <small className='text-body-secondary' style={{fontSize : '.75rem'}}>{trainedFrames} / {frameSize} frames completed</small>
                </div>
                <Card.Footer>
                    <div className="d-flex justify-content-center gap-3 ">
                        
                        <div>
                            <Link className="btn-sm btn btn-primary"  to={`/workspace/${project['_id']['$oid']}`}>
                            Open Project
                            </Link>
                        </div>
                        <div>
                            <button className="btn-sm btn btn-danger" onClick={(e) => buttonHandler(e, project)}>
                            Delete Project
                            </button>
                        </div>
                    </div>
                </Card.Footer>
            </Card>
        </div>
    );
}

export default ProjectCard;

