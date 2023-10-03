import AIOption from './AIOption';
import AIBox from './AIBox';
import InfoLabel from './InfoLabel';
import OptionsBox from './OptionsBox';


const AnnotationBox = (props)=>{

return(
    <div className='btns-box'>
        {/*  annotation tools */}
        <AIOption onSaveAnnotations = {props.onSaveAnnotations} draw={props.draw} showModal={props.showModal} isModalShown={props.isModalShown} />
        {/* Frames, suggestions */}
        <AIBox setIsNewFrame={props.setIsNewFrame}/>
        {/* Annotation labels */}
        <InfoLabel />
        {/* Settings, Save, discard */}
        <OptionsBox showModal={props.showModal} isModalShown={props.isModalShown}/>
    </div>
)
}
export default AnnotationBox