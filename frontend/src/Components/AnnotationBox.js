import AIOption from './AIOption';
import AIBox from './AIBox';
import InfoLabel from './InfoLabel';
import OptionsBox from './OptionsBox';


const AnnotationBox = (props)=>{

return(
    <div className='btns-box'>
        {/*  annotation tools */}
        <AIOption onSaveAnnotations = {props.onSaveAnnotations} draw={props.draw} showModal={props.showModal} isModalShown={props.isModalShown}/>
        {/* Frames, suggestions */}
        <AIBox moveForward={props.moveForward} moveBackwards={props.moveBackwards} counter = {props.counter}/>
        {/* Annotation labels */}
        <InfoLabel />
        {/* Settings, Save, discard */}
        <OptionsBox />
    </div>
)
}
export default AnnotationBox