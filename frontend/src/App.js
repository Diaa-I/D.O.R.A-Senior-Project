import './App.css';
import React, { useState, useRef, useEffect} from 'react';
import Canvas from './Components/Canvas';
import AnnotationBox from './Components/AnnotationBox';
import axios from 'axios';



const INITIAL_Annotations = [];
let current_shape_index = 0;


function App() {
  let colors = ['red','blue','green']
  const canvasRef = useRef(null)
  const contextRef = useRef(null)

  
  
  const [Annotations,setAnnotations]=useState(INITIAL_Annotations)
  const [frame,setFrames] = useState(0)
  const [isNewFrame,setIsNewFrame] = useState(false)


  if(isNewFrame){
      // We probably will need a state called isNewFrame 
  // So when we change frames, it saves the old annotations, and then sets the annotations state into emtpy array
  // and displays 0 annotations on the screen
    contextRef.current.clearRect(0,0,canvasRef.current.width,canvasRef.current.height);
    // Before deleteing the frames, we need to save them call the function that saves them
    setAnnotations([])
    setIsNewFrame(false)
  }

 
  useEffect(()=>{
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d')
    contextRef.current = context
    canvasRef.current.onmousedown = mouse_down
    draw_img()
  },[])
    

    console.log("Yo")
  const btnToDraw=()=>{
    draw(contextRef,colors[Math.floor(Math.random() * colors.length)])  
  }


  const onSaveAnnotations = (newAnnotation)=>{
    setAnnotations((prevAnnotations)=>{return[newAnnotation,...prevAnnotations]})
  }
  
  const onFrameChangeForward = ()=>{
    setFrames((prevframe)=>{return prevframe + 1})
    setIsNewFrame(true)
  }
  const onFrameChangeBackwards = ()=>{
    setFrames((prevframe)=>{return prevframe>0 ? prevframe - 1 : 0})
    setIsNewFrame(true)
  }
  const draw = (context,color)=>{
    contextRef.current.clearRect(0,0,canvasRef.current.width,canvasRef.current.height);
    for(let annotation of Annotations){
      console.log('---------------------')
      console.log(annotation)
      console.log('---------------------')
      contextRef.current.fillStyle = color
      contextRef.current.fillRect(annotation.x,annotation.y,annotation.width,annotation.height)
  }
}
  const draw_img = ()=>{
    var image = new Image();
    image.src = "https://images.unsplash.com/photo-1682213916353-279defcd3003?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80";
    image.onload = () => {
      contextRef.current.drawImage(image, 0, 0);
    };
// background.src = "/src/zero-take-3uI_GYlGT6s-unsplash.jpg";
//     contextRef.current.drawImage(background, 10, 10);
  }
const is_mouse_in_box = (x,y,annotation)=>{
  console.log(x,y,annotation)
  let annotation_left = annotation.x;
  let annotation_right = annotation.x + annotation.width;
  let annotation_top = annotation.y;
  let annotation_bottom = annotation.y + annotation.height;

  console.log(annotation_left,annotation_right,annotation_left,annotation_bottom)
  if(x > annotation_left && x < annotation_right && y > annotation_top && y < annotation_bottom){
    console.log("True")
    return true
  }
  return false
}
const mouse_down = (event)=>{
  event.preventDefault();

  if(Annotations.length>0){


  let startX = parseInt(event.clientX);
  let startY = parseInt(event.clientY);
  let index = 0;
  console.log(Annotations)

  for(let annotation of Annotations){
    if(is_mouse_in_box(startX,startY,annotation)){
      console.log("Yeah")
      current_shape_index = index;
    }else{
    console.log("No")
  }
  index++;
  }
} 
}

if(Annotations.length>0) canvasRef.current.onmousedown = mouse_down
console.log('////////////////////////////////')
console.log(isNewFrame)
console.log(Annotations)
console.log('////////////////////////////////')

  return (
    <div class="background">
      <Canvas Annotations={Annotations}   forwardRef={canvasRef}  />
        {/* Maybe we contain all of them in one box */}
      <AnnotationBox   draw={btnToDraw}   onSaveAnnotations = {onSaveAnnotations} moveForward={onFrameChangeForward} moveBackwards={onFrameChangeBackwards} counter={frame}/>
    </div>
  );
}

export default App;


        
            