import './workspace.css'


const OptionsBox = (props)=>{
    return(
        <div className='d-flex flex-column'>
            <button class="btn btn-primary me-2 align-self-center rounded-pill" onClick={props.check_training}>Check Training</button>
            <button class="btn btn-primary me-2 mt-3 align-self-center rounded-pill" onClick={props.export_project}>Export Annotations</button>
        </div>
    )
}

export default OptionsBox