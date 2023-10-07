import React, { useState, useRef, useEffect} from 'react';
import Canvas from './Canvas';
import AnnotationBox from './AnnotationBox';
import axios from 'axios';
import '../../App.css';
const INITIAL_Annotations = [];
let current_shape_index = 0;


export default function Workspace(props){
  // All Related to canvas manipulation 
    let defaultImageMetadata = {width:"1400px",height:"850px"}
    var startX,startY = 0
    var dragTR,dragTL,dragBR,dragBL = false
    // Image related canvas
    const imageCanvasRef = useRef(null)
    const imageContextRef = useRef(null)

    // Annotation related canvas
    const annotationCanvasRef = useRef(null)
    const annotationContextRef = useRef(null)

    // MetaData of image
    const [imageMetadata,setImageMetaData] = useState(defaultImageMetadata)

    // To display and hide modal 
    const [isModalShown,setIsModalShown] = useState(false)

    // Annotations array  
    const [Annotations,setAnnotations]=useState(INITIAL_Annotations)

    // Has the user requested to go back or infront (a new frame request)
    const [isNewFrame,setIsNewFrame] = useState(true)

    // Has the user requested to get the frame before this one
    const [isGoingBack,setIsGoingBack] = useState(false)

    // Is the all the data retrieved (IS Loading)
    const [isLoading,setIsLoading] = useState(true)

    // Labels array
    const [Labels,setLabels] = useState([])
    
    // Used to check if the user is moving mouse when inside the Annotation
    var check = {"isMoving":true}
  
  
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
      // Have a request here to get all location of frames
      // Then save them into frames
      // Whenever new frame is there then move based on that
      // Maybe we can have another state called currentFrame
      // Which is like pointer to which frame stored in the another state called frames which are requested first

    },[])
  
    useEffect(()=>{
        // We probably will need a state called isNewFrame 
      // So when we change frames, it saves the old annotations, and then sets the annotations state into emtpy array
      // and displays 0 annotations on the screen
      console.log(isNewFrame,isGoingBack)
      if(isNewFrame && !isGoingBack){
        console.log('THIS ONE ')
      imageContextRef.current.clearRect(0,0,imageCanvasRef.current.width,imageCanvasRef.current.height);
      // Before deleteing the frames, we need to save them call the function that saves them
      // Counter how many frames we have used from the one locally called 
      // Actually if we are getting their directories we can get all 
      // If we will be using GridFS then maybe we do counter but if directories then all.
      // That is moving forward we get all, but backwards then it will be retireval from back
      console.log("Hello")
      setAnnotations([])
      setIsNewFrame(false)
      // SEND ANNOTATIONS WITH WHICH FRAME NUMBER THIS IS 
      if(Annotations.length!=0){
      axios.post("http://localhost:5000/workspace/save_annotation",Annotations).then((response)=>{
      console.log(response)
      axios.get("http://localhost:5000/workspace/retrieve_next_batch?starting_from=0&retrieval_size=1").then(res=>{
      var image = new Image();
      image.src = res.data['Image_Dir']
      image.onload = () => {
        imageContextRef.current.drawImage(image, 0, 0);

      //   if(image.width>1920 && image.height>1080){
      //     setImageMetaData({width:"1920px",height:"1080px"})
      // }
      // else{
      //   setImageMetaData({width:image.width,height:image.height})
      // }
      }
      
    })
    })
  }
  else{
    console.log("WHY")
    axios.get("http://localhost:5000/workspace/retrieve_next_batch?starting_from=0&retrieval_size=1").then(res=>{
      var image = new Image();
      image.src = res.data['Image_Dir']
     
      image.onload = () => {
        imageContextRef.current.drawImage(image, 0, 0);
      } 
      setAnnotations([])
      setIsNewFrame(false)
      
    
    })
  }
  }
  else if (isNewFrame && isGoingBack){
    axios.get("http://localhost:5000/workspace/retrieve_previous_batch").then(res=>{
      console.log(res)
      var image = new Image();
      image.src = res.data['Image_Dir']
      console.log("HEEEE")
      image.onload = () => {
        imageContextRef.current.drawImage(image, 0, 0);
      } 
      // Check If no annotation was present in the last frame if there is then display them if not then don't display anything (Displaying is by setting the Annotation state to either the old annotations or nothing which will trigger the useEffect that renders whenever Annotations change)
      if(res.data['Annotations']){
      setAnnotations([...res.data['Annotations']])
    }

    else{
      setAnnotations([])
    }
      setIsNewFrame(false)
      setIsGoingBack(false)
    })
      }
    },[imageContextRef,isNewFrame])
  
    useEffect(()=>{
      annotationCanvasRef.current.onmousedown = mouse_down
      annotationCanvasRef.current.onmouseup = mouse_up
      annotationCanvasRef.current.onmouseout = mouse_out
      annotationCanvasRef.current.onmousemove = mouse_move
      annotationCanvasRef.current.oncontextmenu = onContextMenuHandler
      console.log(Annotations)
      if (Annotations&&Annotations.length>0){
        draw() 
      }
      else{
        draw()
      }
  
    },[Annotations])

  // return if distance between 2 points is less than 10
  let checkCloseEnough = function(p1, p2) {
    return Math.abs(p1 - p2) < 10;
  }  
  
    // const btnToDraw=(newAnnotation)=>{
    //   // let newAnnotation = {x:200, y:50, width:100, height: 150,"selected":false}
    //   // setAnnotations((prevAnnotations)=>{return[newAnnotation,...prevAnnotations]})
    //    draw()
    // }
  
    function onContextMenuHandler(e) {
      e.preventDefault();
      // To delete the annotation
      startX = parseInt(e.offsetX)
      startY = parseInt(e.offsetY)
        
      for(let Annotation of Annotations){
          if(is_mouse_in_Annotation(startX, startY, Annotation)){
            // To remove Annotation right clicked on 
            let tempAnnotation = [...Annotations]
            tempAnnotation = tempAnnotation.filter(current=>{
              return current!==Annotation
            })
            setAnnotations(tempAnnotation)
              break
          }
      }
  
  };
  
  
    const onSaveAnnotations = (newAnnotation)=>{
      setAnnotations((prevAnnotations)=>{return[newAnnotation,...prevAnnotations]})
    }
    

  
    const draw = ()=>{
  
      // Clear the canvas, Clears specified pixels within a rectangle
      annotationContextRef.current.clearRect(0,0,annotationCanvasRef.current.width,annotationCanvasRef.current.height);
      // For all the annotations display a square box
      for(let annotation of Annotations){ 
        annotationContextRef.current.strokeStyle = "yellow"
        annotationContextRef.current.beginPath();
        annotationContextRef.current.rect(annotation.x,annotation.y,annotation.width,annotation.height); 
        annotationContextRef.current.stroke(); 
        annotationContextRef.current.closePath();
        // Color of the box, 	Sets or returns the color, gradient, or pattern used to fill the drawing
        // annotationContextRef.current.fillStyle = "black"
        // // Placing the annotation in the right place, fillRect Draws a "filled" rectangle, strokeRect()	Draws a rectangle (with no fill)
        // annotationContextRef.current.fillRect(annotation.x,annotation.y,annotation.width,annotation.height)
    }
  }
  
  const is_mouse_in_Annotation = (x,y,annotation)=>{
    // the location of where I am clicking (inside the box) and inside the box give very different results
    let annotation_left = annotation.x;
    let annotation_right = annotation.x + annotation.width;
    let annotation_top = annotation.y;
    let annotation_bottom = annotation.y + annotation.height;
  
    if(x > annotation_left && x < annotation_right && y > annotation_top && y < annotation_bottom){
      return true
    }
    return false
  }
  
  const update_shape_props = function(shape){
    if (shape.x < 0)
        shape.x = 0
    if (shape.y < 0)
        shape.y = 0
    if (shape.width < 0){
        shape.width = -1*shape.width;
        shape.x = shape.x - shape.width;
    }
     if (shape.height < 0){
        shape.height = -1*shape.height;
        shape.y = shape.y - shape.height;
     }
  }
  
  
  const mouse_down = (event)=>{
    event.preventDefault();
  
    if(Annotations.length>0){
      startX = parseInt(event.offsetX)
      startY = parseInt(event.offsetY)
     // Only move when left click is clicked on mouse
      switch (event.which) {
          case 1:
      for(let Annotation of Annotations){
          if(is_mouse_in_Annotation(startX, startY, Annotation)){
              const myNextList = [...Annotations];
              const annotation = myNextList.find(
              a => a === Annotation
              );
              annotation.selected = true;
              annotationCanvasRef.current.style.cursor = "move"
              check.isMoving = true
              setAnnotations(myNextList)
              return 
          }
          else {
              // 1. top left
              if (checkCloseEnough(startX, Annotation.x) && checkCloseEnough(startY, Annotation.y)){
                  dragTL = true;
                  annotationCanvasRef.current.style.cursor = "nw-resize"
                  Annotation.selected = true
                  return 
              }
              // 2. top right
              else if (checkCloseEnough(startX, Annotation.x + Annotation.width) && checkCloseEnough(startY, Annotation.y)){
                  dragTR = true;
                  annotationCanvasRef.current.style.cursor = "ne-resize"
                  Annotation.selected = true
                  return 
              }
              // 3. bottom left
              else if (checkCloseEnough(startX, Annotation.x) && checkCloseEnough(startY, Annotation.y + Annotation.height)){
                  dragBL = true;
                  annotationCanvasRef.current.style.cursor = "sw-resize"
                  Annotation.selected = true
                  return 
              }
              // 4. bottom right
              else if (checkCloseEnough(startX, Annotation.x + Annotation.width) && checkCloseEnough(startY, Annotation.y + Annotation.height)){
                  dragBR = true;
                  annotationCanvasRef.current.style.cursor = "se-resize"
                  Annotation.selected = true
                  return 
              }
              
          }
      }
  
      break
  }
    }
  }
  // Released the mosue click
  const mouse_up = ((event)=>{
      for(let Annotation of Annotations){
          if (Annotation.selected == true){
              Annotation.selected = false
              update_shape_props(Annotation)   
          }
      }
      
      event.preventDefault()
      check.isMoving = false
      startX = parseInt(event.offsetX)
      startY = parseInt(event.offsetY)
      dragTL = dragTR = dragBL = dragBR = false;
      annotationCanvasRef.current.style.cursor = 'default'
  })
  
  // Went outside the canvas
  let mouse_out = function(event){
    if(!check.isMoving){
        return; 
    }
    event.preventDefault()
    for(let Annotation of Annotations){
        if (Annotation.selected == true){
            Annotation.selected = false
        }
    }
    check.isMoving  = false
    dragTL = dragTR = dragBL = dragBR = false;
    annotationCanvasRef.current.style.cursor = 'default'
  }
  
  const mouse_move = (event)=>{
    
      event.preventDefault()
      let mouseX = parseInt(event.offsetX)
      let mouseY = parseInt(event.offsetY)
      if(!check.isMoving){
          for(let Annotation of Annotations){
  
              if (Annotation.selected == true){
  
              // 1. resize from top-left
              if (dragTL){
                  Annotation.width += Annotation.x - mouseX;
                  Annotation.height += Annotation.y - mouseY;
                  Annotation.x = mouseX;
                  Annotation.y = mouseY;
                  startX = mouseX
                  startY = mouseY
                  draw()
              }
              // 2. resize from top-right
              else if (dragTR){
                  Annotation.width += mouseX - (Annotation.x + Annotation.width);
                  Annotation.height += Annotation.y - mouseY;
                  Annotation.y = mouseY;
                  startX = mouseX
                  startY = mouseY
                  draw()
              }
              // 3. resize from bottom-right
              else if (dragBR){
                  Annotation.width += mouseX - (Annotation.x + Annotation.width);
                  Annotation.height += mouseY - (Annotation.y + Annotation.height);
                  startX = mouseX
                  startY = mouseY
                  draw()
              }
              // resize from bottom-left
              else if (dragBL){
                  Annotation.width += Annotation.x - mouseX;
                  Annotation.height += mouseY - (Annotation.y + Annotation.height);
                  Annotation.x = mouseX;
                  startX = mouseX
                  startY = mouseY
                  draw()
              }
          } 
      }
  }
      else {
          for(let Annotation of Annotations){
          if (Annotation.selected == true){
          // move across canvas, following cursor
          Annotation.x = mouseX;
          Annotation.y = mouseY;
          startX = mouseX;
          startY = mouseY;
          let current_Annotation = Annotation;
          current_Annotation.x = mouseX;
          current_Annotation.y = mouseY;
          draw();
          return
      }
  }
      
  
   
  }
  }

    return(
        <div>
        <Canvas Annotations={Annotations}   forwardRef={imageCanvasRef} annotationCanvasRef={annotationCanvasRef} imageMetadata={imageMetadata} onContextMenuHandler={onContextMenuHandler} />
        <AnnotationBox   setIsGoingBack={setIsGoingBack} draw={draw}   onSaveAnnotations = {onSaveAnnotations} setIsNewFrame={setIsNewFrame} showModal={props.showModal} isModalShown={props.isModalShown}/>
        </div>
    )
}