import React, { useState, useRef, useEffect} from 'react';
import Canvas from './Canvas';
import AnnotationBox from './AnnotationBox';
import axios from 'axios';
import '../../App.css';
import { useParams } from 'react-router-dom';
const INITIAL_Annotations = [];
let current_shape_index = 0;

// const imageBitmap: ImageBitmap = await createImageBitmap(blob); // Blob file
// const { width, height } = imageBitmap;


export default function Workspace(props){
  // All Related to canvas manipulation 
    let defaultImageMetadata = {width:"1250",height:"650"}
    var startX,startY = 0
    var dragTR,dragTL,dragBR,dragBL = false
    
    // Image related canvas
    const imageCanvasRef = useRef(null)
    const imageContextRef = useRef(null)

    // Get the specific project in the workspace
    const { id:project_id } = useParams()

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

    // Which frame we are at
    const [frameCounter,setFramesCounter] = useState(0)
    // How many frames in the project
    const [framesSize,setFramesSize] = useState('')
    // CurrentFrame
    const [currentFrame,setCurrentFrame] = useState()
    // Just Loaded for first time or Get New Batch of Frames
    const [getNewFrames,setGetNewFrames] = useState(true)
    // Frames Directory list contains all the directories of the frames
    const [frames,setFrames] = useState([])

    // KEEP TRACK OF WHICH FRAME WAS Annotated
    // Either each one that has an annotation and was not deleted then save that frame number into a list and is checked once we go back and front
    // OR Once you skip something that counts as being annotated
    //GET NUMBER WHERE WE HAVE TO GET NEW FRAMES BUT THIS IS NOT FOR DIRECTORIES
    // Used to check which frames have been annotated so they can be used to retireve the annotations
    const [annotatedFrames,setAnnotatedFrames] = useState([])

    // When to train the model (Should we have array or Should we have one by one)
    const [shouldTrain,setShouldTrain] = useState([])

    // Used to check if the user is moving mouse when inside the Annotation
    var check = {"isMoving":true}

    console.log(project_id)

    // When page is first loaded
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
      axios.get(`http://localhost:5000/workspace/get_project_information/${project_id}`).then((res)=>{
             // Negative because we starting from 0, so 0-9 is 10 
        // Maybe for user experience we can start from 10
        setFramesSize(res.data.Frames-1)
        // How will we divide it maybe first we do 500 then 100 + 100 + 100 + 50 + 50
        // IT HAS PROBLEMS WHAT IF I WENT FRONT THEN BACK
        setShouldTrain((res.data.Frames/2) -1)
        // maybe when we reach the shouldTrain then event to send to api and then give them access to start again 
        // 
        setIsLoading(false)
      })

    },[])
  
    useEffect(()=>{
      // Check if get you need to get frames
      // FrameNumber is the last frame ur at
      // FrameCounter is this frame ur at 
      if(getNewFrames){
        // Make a request to get frames
        axios.get(`http://localhost:5000/workspace/retrieve_next_batch/${project_id}`).then(response=>{
        var image = new Image();
        console.log(response.data)
        // Get the frames 
        setFrames(response.data['Image_Dir'])
        // If more than one photo
        if(response.data['Image_Dir'].length>1){
        setCurrentFrame(response.data['Image_Dir'][0]['image_loc'])
        }
        // If only one photo
        else{
          setCurrentFrame(response.data['Image_Dir']['image_loc'])
        }
        image.src = response.data['Image_Dir']['image_loc']
        image.onload = () => {
          imageContextRef.current.drawImage(image, 0, 0,frames[frameCounter]['width'],frames[frameCounter]['height']);
          setImageMetaData({'width':frames[frameCounter]['width'],'height':frames[frameCounter]['width']})  
      }
      // Don't request new frames from API
      setGetNewFrames(false)
      // setIsLoading(false)
      })
      }
      
      // Going forward what shall be requested
      else if(isNewFrame){
        imageContextRef.current.clearRect(0,0,imageCanvasRef.current.width,imageCanvasRef.current.height);
        // Check if this frame is in the annotatedFrames
        var image = new Image();
        image.src = currentFrame
        image.onload = () => {
          imageContextRef.current.drawImage(image, 0, 0,frames[frameCounter]['width'],frames[frameCounter]['height']);
          setImageMetaData({'width':frames[frameCounter]['width'],'height':frames[frameCounter]['width']})  

        }

        // Framenumber so we can send data to API to save annotations 
        let frameNumber = frameCounter - 1
        if(isGoingBack){
           frameNumber = frameCounter + 1
        }

        if(annotatedFrames.indexOf(frameNumber)!=-1){
        // Get annotations of the frame using frameCounter because frameNumber is used for the last frame you were at the counter is the one you are currently at
        // Check the page has been annotated (yes)

        if(Annotations.length!=0){
          // Save the annotations made by user
          axios.post(`http://localhost:5000/workspace/save_annotation`,{frameNumber,Annotations,project_id}).then((res)=>console.log(res))
          setAnnotations([])
          setIsNewFrame(false)
         }
        // Check the page has been annotated(no)
        else{
          // Send to API to delete The Annotations data of this frame from DB

          axios.post(`http://localhost:5000/workspace/delete_annotation`,{frameNumber,Annotations,project_id})
          // Remove this frame from annotatedFrames
          setAnnotatedFrames(annotatedFrames.filter((frame)=>{
            return frame!=frameNumber
          }))
          // Empty the annotation
          setAnnotations([])
          // Move from this frame
          setIsNewFrame(false)
       }
      }
      // Add the frame to annotatedFrames
      else{
        if(Annotations.length!=0){
          axios.post("http://localhost:5000/workspace/save_annotation",{frameNumber,Annotations,project_id})
          // Check if it was already there or not
          if (!annotatedFrames.includes(frameNumber)){
          setAnnotatedFrames((prevstate)=>{
            return ([...prevstate,frameNumber])
          })
        }
        // Save in the frontend which frames have been annotated
      }
        // Empty the annotation
        setAnnotations([])
        // Move from this frame
        setIsNewFrame(false)
      }
      setIsGoingBack(false)

      axios.get(`http://localhost:5000/workspace/retrieve_previous_batch/${project_id}?frameNumber=${frameCounter}`).then(response=>{
      // Display annotations already stored in DB
      setAnnotations([...response.data['Annotations']])
      var image = new Image();
      image.src = currentFrame
      image.onload = () => {
        imageContextRef.current.drawImage(image, 0, 0,frames[frameCounter]['width'],frames[frameCounter]['height']);
        setImageMetaData({'width':frames[frameCounter]['width'],'height':frames[frameCounter]['width']})  
      }
    }).catch((err)=>console.log(err))
    // Whenever we need to train this will run and then the api will call another thing that will run (as of now this is the idea)
      // if(shouldTrain.includes(frameCounter)){
      //   axios.get(`http://localhost:5000/workspace/retrieve_previous_batch?frameNumber=${frameCounter}`).then(response=>{
      //     // Display annotations already stored in DB
      //     setAnnotations([...response.data['Annotations']])
      //     var image = new Image();
      //     image.src = currentFrame
      //     image.onload = () => {
      //       imageContextRef.current.drawImage(image, 0, 0,imageMetadata.width,imageMetadata.height);
      //     }
      //   }).catch((err)=>console.log(err))
      // }
      
    }
    
    },[imageContextRef,isNewFrame,getNewFrames])
  
    // When first loaded and any changes in Annotations
    useEffect(()=>{
      console.log(Annotations)
      annotationCanvasRef.current.onmousedown = mouse_down
      annotationCanvasRef.current.onmouseup = mouse_up
      annotationCanvasRef.current.onmouseout = mouse_out
      annotationCanvasRef.current.onmousemove = mouse_move
      annotationCanvasRef.current.oncontextmenu = onContextMenuHandler
      // Draw annotations whenever there is a change, check the code if-else
      if (Annotations&&Annotations.length>0){
        draw() 
      }
      else{
        draw()
      }
  
    },[Annotations])
  // ---------------------------------------------------------------------------------------------------------------------------------------------
  // Canvas manipulation logic
  // return if distance between 2 points is less than 10
  let checkCloseEnough = function(p1, p2) {
    return Math.abs(p1 - p2) < 10;
  }  
  // Handling right click, for deleting annotations 
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
  
  // Saving and setting state for annotations
    const onSaveAnnotations = (newAnnotation)=>{
      setAnnotations((prevAnnotations)=>{return[newAnnotation,...prevAnnotations]})
    }
    

    // Drawing annotation
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

  //Checking if click is inside the annotation
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

  // When resizing the annotations updating the annotation
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
  
  // When mouse is clicked, if left clicked, check where it is clicked and then determine if resizing or move
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
  // Released the mouse click
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

  // Moving the mouse could be resizing or moving the annotation
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
  // Moving frames forward 
  const onFrameChangeForward = ()=>{
    // A condition to stop at last frame
    if(framesSize>=frameCounter+1){
      setCurrentFrame(frames[frameCounter+1]['image_loc'])
        setFramesCounter((prevframe)=>{return prevframe + 1})
        setIsNewFrame(true)   
    }
  }
  // Moving frames backwards 
  const onFrameChangeBackwards = ()=>{
    // A condition to stop at first frame
    if(!frameCounter-1<0){
        console.log("WORKIng back")
    setCurrentFrame(frames[frameCounter-1]['image_loc'])
    setFramesCounter((prevframe)=>{return prevframe>0 ? prevframe - 1 : 0})
    setIsNewFrame(true)
    setIsGoingBack(true)
}
  }
// Handling requests to make predictions and return the prediction
  const handleMakePrediction = ()=>{
    // Current image to pass to the API
    axios.post(`http://localhost:5000/workspace/trained_model/${project_id}`,{currentFrame})
    .then((res)=>{
      let newAnnotation = []
      for (let anno of res.data){
        newAnnotation.push({
          "x":anno['x'],
          "y":anno['y'],
          "width":anno['w'],
          "height":anno['h'],
          "label":anno['label'],
          'frame':frameCounter,
          "project_id":project_id
        })
      }
      console.log(newAnnotation)
      setAnnotations((prevAnnotations)=>{return[...newAnnotation,...prevAnnotations]})
      console.log(Annotations)
    })
    .catch((err)=>{console.log(err)})
  }

    return(
        <div>
        <Canvas Annotations={Annotations}   forwardRef={imageCanvasRef} annotationCanvasRef={annotationCanvasRef} imageMetadata={imageMetadata} onContextMenuHandler={onContextMenuHandler} />
        <AnnotationBox handleMakePrediction={handleMakePrediction} isLoadingAIBOX={isLoading} framesSize={framesSize} frameCounter={frameCounter} onFrameChangeForward={onFrameChangeForward} onFrameChangeBackwards={onFrameChangeBackwards}  draw={draw}   onSaveAnnotations = {onSaveAnnotations}  showModal={props.showModal} isModalShown={props.isModalShown}/>
        </div>
    )
}