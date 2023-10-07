import './workspace.css'


const OptionsBox = (props)=>{
    return(
        <div class="options-box">
            <button class="settings-button" onClick={props.showModal}>Settings</button>
            <button class="save-button" onClick={props.showModal}>Save</button>
            <button class="discard-button" onClick={props.showModal}>Discard Annotations</button>
        </div>
    )
}

export default OptionsBox