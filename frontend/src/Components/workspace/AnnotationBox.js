import AIOption from './AIOption';
import AIBox from './AIBox';
import OptionsBox from './OptionsBox';

import 'bootstrap/dist/css/bootstrap.css';

const AnnotationBox = (props)=>{

return(
    <div className='btns-box pt-3 pb-3'>
    <div className='container'>
        <div className='row justify-content-center'>
            {/* Annotation tools on the left */}
            <div className='col-3'>
                <AIOption setLabelsCounter={props.setLabelsCounter} project_id={props.project_id} onSaveAnnotations={props.onSaveAnnotations} draw={props.draw} showModal={props.showModal} isModalShown={props.isModalShown} />
            </div>

            {/* AIBox in the center */}
            <div className='col-6 text-center'>
                <AIBox handleMakePrediction={props.handleMakePrediction} frameCounter={props.frameCounter} isLoadingAIBOX={props.isLoadingAIBOX} framesSize={props.framesSize} onFrameChangeForward={props.onFrameChangeForward} onFrameChangeBackwards={props.onFrameChangeBackwards} />
            </div>

            {/* OptionsBox on the right */}
            <div className='col-3 align-self-center'>
                <OptionsBox showModal={props.showModal} isModalShown={props.isModalShown} />
            </div>
        </div>
    </div>
</div>
    
)
}
export default AnnotationBox