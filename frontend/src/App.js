import './App.css';
import React, { useState, useRef, useEffect} from 'react';
import axios from 'axios';
import Modal from './Components/utilities/Modal';
import Navbar from './Components/Navbar';



const INITIAL_Annotations = [];
let current_shape_index = 0;


function App() {

  const [isModalShown,setIsModalShown] = useState(false)



 

function showModal(){
  // e.preventDefault()
  console.log("Hello")
  setIsModalShown(true)
}
function hideModal(){
  console.log("Hello")
  setIsModalShown(false)
}
// if(Annotations.length>0){
//    annotationCanvasRef.current.onmousedown = mouse_down
//    annotationCanvasRef.current.onmousedown = mouse_down
//    annotationCanvasRef.current.onmouseup = mouse_up
//    annotationCanvasRef.current.onmouseout = mouse_out
//    annotationCanvasRef.current.onmousemove = mouse_move
// }

  return (
    <div class="background">
      <Modal isModalShown={isModalShown}  hideModal={hideModal} ></Modal>
      <Navbar showModal={showModal}  hideModal={hideModal}/>
    </div>
  );
}

export default App;


        
            