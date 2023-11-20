import { useEffect, useState } from 'react'
import './workspace.css'
import { FaCaretRight , FaCaretLeft } from "react-icons/fa";
import axios from 'axios'

const AIBox = (props)=>{
    // console.log(props)
// const moveBackwards = props.moveBackwards
// const moveForward = props.moveForward
// const counter = props.counter
// const [isLoading,setIsLoading] = useState(true)

// const [frameCounter,setFramesCounter] = useState(0)
// useEffect(()=>{

// },[])

if (props.isLoadingAIBOX){
    return <h1>Loading...</h1>
}
return(
    <div class="ai-decisions-box">
        <div class="navigator">
            <button className='btn btn-light' onClick={props.onFrameChangeBackwards}><FaCaretLeft size={25}></FaCaretLeft></button>
            {/* <svg style="width:30px;" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" stroke="#000000" transform="rotate(270)"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>triangle-filled</title> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="drop" fill="#000000" transform="translate(32.000000, 42.666667)"> <path d="M246.312928,5.62892705 C252.927596,9.40873724 258.409564,14.8907053 262.189374,21.5053731 L444.667042,340.84129 C456.358134,361.300701 449.250007,387.363834 428.790595,399.054926 C422.34376,402.738832 415.04715,404.676552 407.622001,404.676552 L42.6666667,404.676552 C19.1025173,404.676552 7.10542736e-15,385.574034 7.10542736e-15,362.009885 C7.10542736e-15,354.584736 1.93772021,347.288125 5.62162594,340.84129 L188.099293,21.5053731 C199.790385,1.04596203 225.853517,-6.06216498 246.312928,5.62892705 Z" id="Combined-Shape"> </path> </g> </g> </g></svg> */}
        <div>{props.frameCounter} out of {props.framesSize}</div>
            <button className='btn btn-light' onClick={props.onFrameChangeForward}><FaCaretRight size={25}></FaCaretRight></button>
            {/* <svg style="width:30px;" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" stroke="#000000" transform="rotate(90)"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>triangle-filled</title> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="drop" fill="#000000" transform="translate(32.000000, 42.666667)"> <path d="M246.312928,5.62892705 C252.927596,9.40873724 258.409564,14.8907053 262.189374,21.5053731 L444.667042,340.84129 C456.358134,361.300701 449.250007,387.363834 428.790595,399.054926 C422.34376,402.738832 415.04715,404.676552 407.622001,404.676552 L42.6666667,404.676552 C19.1025173,404.676552 7.10542736e-15,385.574034 7.10542736e-15,362.009885 C7.10542736e-15,354.584736 1.93772021,347.288125 5.62162594,340.84129 L188.099293,21.5053731 C199.790385,1.04596203 225.853517,-6.06216498 246.312928,5.62892705 Z" id="Combined-Shape"> </path> </g> </g> </g></svg> */}
        </div>
        {/* <p>{{ filename }}</p> */}

        <button class="btn btn-primary align-self-center mt-3" onClick={props.handleMakePrediction}>Show Suggestions</button>
       
    </div>
)
}

export default AIBox