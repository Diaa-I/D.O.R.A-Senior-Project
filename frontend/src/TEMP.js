import './App.css';
import React, { useState, useRef, useEffect} from 'react';
import Canvas from './Components/Canvas';
import AnnotationBox from './Components/AnnotationBox';
import axios from 'axios';
import Canveseses from './Components/Canveseses';



const INITIAL_Annotations = [];
let current_shape_index = 0;


function App() {
  let defaultImageMetadata = {width:"1400px",height:"850px"}
  let colors = ['red','blue','green']
  // Image related canvas
  const imageCanvasRef = useRef(null)
  const imageContextRef = useRef(null)
  // Annotation related canvas
  const annotationCanvasRef = useRef(null)
  const annotationContextRef = useRef(null)
  // MetaData of image
  const [imageMetadata,setImageMetaData] = useState(defaultImageMetadata)
  
  
  const [Annotations,setAnnotations]=useState(INITIAL_Annotations)
  const [frame,setFrames] = useState(0)
  const [isNewFrame,setIsNewFrame] = useState(true)




 
  useEffect(()=>{
    // Image canvas
    const imageCanvas = imageCanvasRef.current;
    const imageContext = imageCanvas.getContext('2d')
    // Use this to put image
    imageContextRef.current = imageContext


    // Annotation canvas
    const AnnotationCanvas = annotationCanvasRef.current;
    // context of Annotation canvas for drawing Annotation
    const contextAnnotation = AnnotationCanvas.getContext('2d')
    // Use this to draw
    annotationContextRef.current = contextAnnotation
    annotationCanvasRef.current.onmousedown = mouse_down
    // Load the image or video


  },[])

  useEffect(()=>{
      // We probably will need a state called isNewFrame 
    // So when we change frames, it saves the old annotations, and then sets the annotations state into emtpy array
    // and displays 0 annotations on the screen
    console.log(isNewFrame)
    if(isNewFrame){
    imageContextRef.current.clearRect(0,0,imageCanvasRef.current.width,imageCanvasRef.current.height);
    // Before deleteing the frames, we need to save them call the function that saves them
    setAnnotations([])
    setIsNewFrame(false)
    var image = new Image();
    image.src = "https://images.unsplash.com/photo-1682213916353-279defcd3003?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80";
    image.onload = () => {
      imageContextRef.current.drawImage(image, 0, 0);
      console.log(image.width,image.height)
    //   if(image.width>1920 && image.height>1080){
    //     setImageMetaData({width:"1920px",height:"1080px"})
    // }
    // else{
    //   setImageMetaData({width:image.width,height:image.height})
    // }
    }
    }
  },[imageContextRef,isNewFrame])
    
  

  const btnToDraw=()=>{
    draw(annotationContextRef,colors[Math.floor(Math.random() * colors.length)])  
  }


  const onSaveAnnotations = (newAnnotation)=>{
    setAnnotations((prevAnnotations)=>{return[newAnnotation,...prevAnnotations]})
  }
  
  const onFrameChangeForward = ()=>{
    // Add a condition to stop at last frame
    setFrames((prevframe)=>{return prevframe + 1})
    setIsNewFrame(true)
  }
  const onFrameChangeBackwards = ()=>{
    setFrames((prevframe)=>{return prevframe>0 ? prevframe - 1 : 0})
    setIsNewFrame(true)
  }
  const draw = (context,color)=>{
    // Clear the canvas, Clears specified pixels within a rectangle
    annotationContextRef.current.clearRect(0,0,annotationContextRef.current.width,annotationContextRef.current.height);
    // For all the annotations display a square box
    for(let annotation of Annotations){
      console.log('---------------------')
      console.log(annotation)
      console.log('---------------------')
      annotationContextRef.current.strokeStyle = color
      annotationContextRef.current.beginPath();
      annotationContextRef.current.rect(annotation.x,annotation.y,annotation.width,annotation.height); 
      annotationContextRef.current.stroke(); 
      // Color of the box, 	Sets or returns the color, gradient, or pattern used to fill the drawing
      annotationContextRef.current.fillStyle = color
      // // Placing the annotation in the right place, fillRect Draws a "filled" rectangle, strokeRect()	Draws a rectangle (with no fill)
      // annotationContextRef.current.fillRect(annotation.x,annotation.y,annotation.width,annotation.height)
  }
}

const is_mouse_in_box = (x,y,annotation)=>{
  // the location of where I am clicking (inside the box) and inside the box give very different results
  

  let annotation_left = annotation.x;
  let annotation_right = annotation.x + annotation.width;
  let annotation_top = annotation.y;
  let annotation_bottom = annotation.y + annotation.height;
  console.log(annotation_left,annotation_right,annotation_top,annotation_bottom)
  console.log(x,y)
  if(x > annotation_left && x < annotation_right && y > annotation_top && y < annotation_bottom){
    console.log("True")
    return true
  }
  return false
}
const mouse_down = (event)=>{
  event.preventDefault();

  if(Annotations.length>0){

  // The x and y are working good
  let startX = parseInt(event.offsetX);
  let startY = parseInt(event.offsetY);


  let index = 0;
  for(let annotation of Annotations){
    console.log(annotation)
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
const onmousemove = (event)=>{
  event.preventDefault();

  if(Annotations.length>0){

  // The x and y are working good
  let startX = parseInt(event.offsetX);
  let startY = parseInt(event.offsetY);


  let index = 0;
  for(let annotation of Annotations){
    console.log(annotation)
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

if(Annotations.length>0) annotationCanvasRef.current.onmousedown = mouse_down


  return (
    <div class="background">
      
      <Canvas Annotations={Annotations}   forwardRef={imageCanvasRef} annotationCanvasRef={annotationCanvasRef} imageMetadata={imageMetadata} />
        {/* Maybe we contain all of them in one box */}
      {/* <Canveseses ></Canveseses> */}
      <AnnotationBox   draw={btnToDraw}   onSaveAnnotations = {onSaveAnnotations} moveForward={onFrameChangeForward} moveBackwards={onFrameChangeBackwards} counter={frame}/>
      
    </div>
  );
}

export default App;


        
            