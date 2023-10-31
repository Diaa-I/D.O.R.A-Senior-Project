import React from 'react';
import {Card} from 'react-bootstrap';
import { Link } from 'react-router-dom';

function ProjectCard({ project }) {
    return (
        <div className="col">
            <Card style={{ width: '18rem' }}>
                <div className="card-body">
                    <h5 className="card-title">{project.Name}</h5>
                    <p className="card-text">Labels: {project.Labels}</p>
                    <Link  className="btn btn-primary" to={`/workspace/${project['_id']['$oid']}`}>Link to Workspace</Link>
                </div>
            </Card>
        </div>
    );
}

export default ProjectCard;
