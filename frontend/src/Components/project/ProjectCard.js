import React from 'react';
import {Card} from 'react-bootstrap';

function ProjectCard({ project }) {
    return (
        <div className="col">
            <Card style={{ width: '18rem' }}>
                <div className="card-body">
                    <h5 className="card-title">{project.name}</h5>
                    <p className="card-text">Labels: {project.labels}</p>
                    <a href="#" className="btn btn-primary">
                        Open Project
                    </a>
                </div>
            </Card>
        </div>
    );
}

export default ProjectCard;
