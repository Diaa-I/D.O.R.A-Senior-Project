import './workspace.css'


const OptionsBox = (props)=>{
    return(
        <div className='d-flex'>
            <button class="btn btn-primary me-2 align-self-center rounded-pill" onClick={props.showModal}>Check Training</button>
        </div>
    )
}

export default OptionsBox