import { useEffect, useState } from 'react'
import { BsBoundingBoxCircles } from 'react-icons/bs';
import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';


function AIBox (props) {
 const [labels,setLabels] = useState([])
 const [isDraw,setisDraw] = useState(false)
 const [isLoading,setIsLoading] = useState(true)
 const [selectedLabel,setSelectedLabel] = useState(null)
 const [isFirstTime,setIsFirstTime] = useState(true)


useEffect(()=>{

    axios.get(`http://localhost:5000/workspace/${props.project_id}/getlabels`).then((response) => {
    let annotationLabels = [...response.data.labels]
    setLabels([...response.data.labels]);
    let labelsObj = {}
    for (let label of annotationLabels){
        labelsObj[label] = 0
    }
    props.setLabelsCounter(labelsObj)
    setIsLoading(false);
  });

    // setlabels(["A","B"]);
    // setIsLoading(false);

    // When labels are changed in set labels
    // Then make an object counter for each label
    // each time a label is added a counter + 1 
},[])
    
  

  if(!isLoading && isFirstTime){
  setSelectedLabel(labels[0])
  setIsFirstTime(false)
}



//   console.log(labels)
//   console.log(isLoading)
    // if(isDraw){
    //     props.draw(props.Annot)
    //     setisDraw(false)
    // }



    function squareHandler(event){
        event.preventDefault()
        //  When button is pressed then we pass data from child to parent, then go to canvas and draw a shape
       let Annotation = ({"x":10,"y":10,"width":100,"height":100,"label":selectedLabel})

        props.onSaveAnnotations(Annotation)
        // setisDraw(true)
        props.draw()

    }
    function select_handler(event){
        setSelectedLabel(event.target.value)
    }

    return( 
    <div className='d-flex align-items-baseline flex-column'>
        <select className='form-control ms-2 mb-2' name="select label" id=""  onChange={select_handler} value={selectedLabel}>
            {labels.map(label=>(
                <option value={label}>{label}</option>
                ))}
        </select>
        
            <button className='btn btn-primary mt-3' onClick={squareHandler}  ><BsBoundingBoxCircles size={25} /></button>
    </div>
    )







    {/* <div className="ai-decisions-box">
        <div className="navigator">
            <svg style="width:30px;" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" stroke="#000000" transform="rotate(270)"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>triangle-filled</title> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="drop" fill="#000000" transform="translate(32.000000, 42.666667)"> <path d="M246.312928,5.62892705 C252.927596,9.40873724 258.409564,14.8907053 262.189374,21.5053731 L444.667042,340.84129 C456.358134,361.300701 449.250007,387.363834 428.790595,399.054926 C422.34376,402.738832 415.04715,404.676552 407.622001,404.676552 L42.6666667,404.676552 C19.1025173,404.676552 7.10542736e-15,385.574034 7.10542736e-15,362.009885 C7.10542736e-15,354.584736 1.93772021,347.288125 5.62162594,340.84129 L188.099293,21.5053731 C199.790385,1.04596203 225.853517,-6.06216498 246.312928,5.62892705 Z" id="Combined-Shape"> </path> </g> </g> </g></svg>
            <div>44 out of 1244</div>
            <svg style="width:30px;" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" stroke="#000000" transform="rotate(90)"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>triangle-filled</title> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="drop" fill="#000000" transform="translate(32.000000, 42.666667)"> <path d="M246.312928,5.62892705 C252.927596,9.40873724 258.409564,14.8907053 262.189374,21.5053731 L444.667042,340.84129 C456.358134,361.300701 449.250007,387.363834 428.790595,399.054926 C422.34376,402.738832 415.04715,404.676552 407.622001,404.676552 L42.6666667,404.676552 C19.1025173,404.676552 7.10542736e-15,385.574034 7.10542736e-15,362.009885 C7.10542736e-15,354.584736 1.93772021,347.288125 5.62162594,340.84129 L188.099293,21.5053731 C199.790385,1.04596203 225.853517,-6.06216498 246.312928,5.62892705 Z" id="Combined-Shape"> </path> </g> </g> </g></svg>
        </div>
        <p>{{ filename }}</p>
        <div>
            <button className="resuggest">Show Suggestions</button>
            <button className="accept">Accept All</button>
            <button className="reject">Reject All</button>
        </div>
    </div> */}
}


export default AIBox;