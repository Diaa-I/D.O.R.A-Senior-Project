import { useEffect, useState } from 'react'

import './workspace.css'
import axios from 'axios';


function AIBox (props) {
 const [labels,setLabels] = useState([])
 const [isDraw,setisDraw] = useState(false)
 const [isLoading,setIsLoading] = useState(true)
 const [selectedLabel,setSelectedLabel] = useState(null)
 const [isFirstTime,setIsFirstTime] = useState(true)


useEffect(()=>{
axios.get('http://localhost:5000/workspace/getlabels').then((response) => {
    // console.log([...response.data.labels])
    setLabels([...response.data.labels]);
    setIsLoading(false);
  });

    // setlabels(["A","B"]);
    // setIsLoading(false);

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
       let Annotation = ({"x":10,"y":10,"width":100,"height":100,"color":"red","label":selectedLabel})

        props.onSaveAnnotations(Annotation)
        // setisDraw(true)
        props.draw()

    }
    function select_handler(event){
        setSelectedLabel(event.target.value)
    }

    return( 
    <div class="ai-options-box" >
        <select name="select label" id=""  onChange={select_handler} value={selectedLabel}>
            {labels.map(label=>(
                <option value={label}>{label}</option>
                ))}
        </select>
        <div >
            <button onClick={squareHandler} class="square" ><svg fill="#000000" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>square</title> <path d="M28 24v4h-4v-1h-16v1h-4v-4h1v-16h-1v-4h4v1h16v-1h4v4h-1v16h1zM5 27h2v-2h-2v2zM7 5h-2v2h2v-2zM24 7h-16v1h-1v16h1v1h16v-1h1v-16h-1v-1zM27 5h-2v2h2v-2zM25 25v2h2v-2h-2z"></path> </g></svg></button>
            <button class="polygon" onClick={props.showModal}><svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M14 40C15.1046 40 16 39.1046 16 38C16 36.8954 15.1046 36 14 36C12.8954 36 12 36.8954 12 38C12 39.1046 12.8954 40 14 40ZM14 42C16.2091 42 18 40.2091 18 38C18 35.7909 16.2091 34 14 34C11.7909 34 10 35.7909 10 38C10 40.2091 11.7909 42 14 42Z" fill="#333333"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M10 22C11.1046 22 12 21.1046 12 20C12 18.8954 11.1046 18 10 18C8.89543 18 8 18.8954 8 20C8 21.1046 8.89543 22 10 22ZM10 24C12.2091 24 14 22.2091 14 20C14 17.7909 12.2091 16 10 16C7.79086 16 6 17.7909 6 20C6 22.2091 7.79086 24 10 24Z" fill="#333333"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M38 22C39.1046 22 40 21.1046 40 20C40 18.8954 39.1046 18 38 18C36.8954 18 36 18.8954 36 20C36 21.1046 36.8954 22 38 22ZM38 24C40.2091 24 42 22.2091 42 20C42 17.7909 40.2091 16 38 16C35.7909 16 34 17.7909 34 20C34 22.2091 35.7909 24 38 24Z" fill="#333333"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M34 40C35.1046 40 36 39.1046 36 38C36 36.8954 35.1046 36 34 36C32.8954 36 32 36.8954 32 38C32 39.1046 32.8954 40 34 40ZM34 42C36.2091 42 38 40.2091 38 38C38 35.7909 36.2091 34 34 34C31.7909 34 30 35.7909 30 38C30 40.2091 31.7909 42 34 42Z" fill="#333333"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M24 12C25.1046 12 26 11.1046 26 10C26 8.89543 25.1046 8 24 8C22.8954 8 22 8.89543 22 10C22 11.1046 22.8954 12 24 12ZM24 14C26.2091 14 28 12.2091 28 10C28 7.79086 26.2091 6 24 6C21.7909 6 20 7.79086 20 10C20 12.2091 21.7909 14 24 14Z" fill="#333333"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M34.9188 19.028L25.9188 12.5995L27.0812 10.972L36.0812 17.4006L34.9188 19.028ZM21.7844 12.8115L13.0812 19.028L11.9188 17.4006L20.622 11.184L21.7844 12.8115ZM11.6429 22.7831L14.3095 34.7831L12.3572 35.2169L9.69049 23.2169L11.6429 22.7831ZM33.6905 34.7831L36.246 23.2831L38.1984 23.7169L35.6429 35.2169L33.6905 34.7831ZM17 37H31V39H17V37Z" fill="#333333"></path> </g></svg></button>
        </div>
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