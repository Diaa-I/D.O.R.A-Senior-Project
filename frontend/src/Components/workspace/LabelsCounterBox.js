import React from 'react';

export default function LabelsCounterBox(props) {
    const { labelsCounter } = props;
    return (
        <div className="card" style={{ backgroundColor: '#737373', color: '#ffffff' }}>
            <div className='card-header bg-primary text-white'>
            <h6 className="card-title">Label Counts</h6>

            </div>
            <div className="card-body">
                <ul className="list-group">
                    {Object.entries(labelsCounter).map(([label, count]) => (
                        <li key={label} className="list-group-item d-flex justify-content-between align-items-center" style={{ backgroundColor: '#555555', color: '#ffffff' }}>
                            {label}
                            <span className="badge bg-primary">{count}</span>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}