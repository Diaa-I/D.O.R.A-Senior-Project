import React, { useEffect, useState } from 'react';


export default function LabelsCounterBox(props) {
    const { labelsCounter,Annotations,isNewFrame } = props;
    // To set the label of the annotation selected so the user can see it
    const [selectedAnnotation,setSelectedAnnoation] = useState('')
    useEffect(()=>{
        if(isNewFrame){
            // With each frame change delete the previously set label
            setSelectedAnnoation('')
        }
        console.log(Annotations)
        for(let annotation of Annotations){
            if (annotation.selected){
                setSelectedAnnoation(annotation.label)
                break
            }
        }
    },[Annotations,isNewFrame])
    return (
        <div className="card" style={{ backgroundColor: '#737373', color: '#ffffff' }}>
            <div className='card-header bg-primary text-white'>
            <h6 className="card-title">Label Counts & Info</h6>

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
                <div className="alert alert-info mt-3" role="alert">
                        <h6 className="alert-heading">Selected Annotation:</h6>
                        <span className="badge bg-primary">{selectedAnnotation}</span>
                    </div>
                </div>
        </div>
    );
}