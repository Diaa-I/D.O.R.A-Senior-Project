import React, { useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './ProjectCard.css';

function ProjectCard({ project }) {
    const labels = project.Labels || [];

    const [showAllLabels, setShowAllLabels] = useState(false);

    const toggleLabels = () => {
        setShowAllLabels(!showAllLabels);
    };
    console.log(project)
    console.log(project['Directory_of_File']+`/0_${project['Name']}.jpg`)
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
                </Card.Footer>
            </Card>
        </div>
    );
}

export default ProjectCard;

