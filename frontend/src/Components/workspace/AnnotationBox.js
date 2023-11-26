import AIOption from './AIOption';
import AIBox from './AIBox';
import OptionsBox from './OptionsBox';

import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';

const AnnotationBox = (props)=>{
    const export_project = ()=>{
        props.setIsLoading(true)
        axios.post(`http://localhost:5000/export_project/${props.project_id}`)
        .then((res)=>{alert(res.data.Exported_data_location); props.setIsLoading(false)})
        .catch((err)=>{alert(err,"Error occurred"); props.setIsLoading(false)})
    }
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
                <OptionsBox export_project = {export_project} check_training={props.check_training} isModalShown={props.isModalShown} />
            </div>
        </div>
    </div>
</div>
    
)
}
export default AnnotationBox