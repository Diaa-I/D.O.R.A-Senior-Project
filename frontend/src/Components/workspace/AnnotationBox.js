import AIOption from './AIOption';
import AIBox from './AIBox';
import InfoLabel from './InfoLabel';
import OptionsBox from './OptionsBox';

import 'bootstrap/dist/css/bootstrap.css';

const AnnotationBox = (props)=>{

return(
    <div className='btns-box pt-3'>
        {/*  annotation tools */}
        <AIOption setLabelsCounter={props.setLabelsCounter} project_id={props.project_id} onSaveAnnotations = {props.onSaveAnnotations} draw={props.draw} showModal={props.showModal} isModalShown={props.isModalShown} />
        {/* Frames, suggestions */}
        <AIBox handleMakePrediction={props.handleMakePrediction} frameCounter={props.frameCounter} isLoadingAIBOX ={props.isLoadingAIBOX}framesSize={props.framesSize} onFrameChangeForward={props.onFrameChangeForward} onFrameChangeBackwards={props.onFrameChangeBackwards} />
        {/* Annotation labels */}
        {/* <InfoLabel /> */}
        {/* Settings, Save, discard */}
        <OptionsBox showModal={props.showModal} isModalShown={props.isModalShown}/>
    </div>
)
}
export default AnnotationBox