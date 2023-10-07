import './workspace.css'
import {useRef,useEffect} from "react"

const Canvas = (props) => {

    const Annotations = props.Annotations;
    useEffect(()=>{
        // console.log(props)
        // console.log(props.forwardRef)
        // console.log(props.annotationCanvasRef)
        // when it loads in change both canvas sizes to the same as photo size
        // props.forwardRef.current.height = "100px"
        // props.forwardRef.current.width = "100px"
    })

// console.log(props.onContextMenuHandler)   


    return(
    <div className="canvas">
        {/* <p>
            {Annotations.map(el=><ul><li>x:{el.x}</li><li>y:{el.y}</li><li>w:{el.width}</li><li>h:{el.height}</li><li>h:{el.color}</li><li>{el.label}</li></ul>)}
        </p> */}
        {/* When annotations then get printed here */}
        {/* And we loop onclick we can call a function when that happens the values in the rectangle should change */}
        {/* Dont set the canvas width and size in css, it doesnt work  https://stackoverflow.com/questions/15583558/why-is-38px-x-38px-is-bigger-than-a-canvas-rectangle-38-x-38-in-spite-of-being-t https://stackoverflow.com/questions/2588181/canvas-is-stretched-when-using-css-but-normal-with-width-height-attributes https://stackoverflow.com/questions/76389730/canvas-is-drawing-rectangle-bigger-than-my-dimension*/}
        <canvas className="canvas-body" itemID="canvas"  ref={props.forwardRef} width={props.imageMetadata.width} height={props.imageMetadata.height}></canvas>
                                                                                                                                                                                    {/* onContextMenu={props.onContextMenuHandler} */}
        <canvas className="canvas-body body-annotation" itemID="canvas-annotation"ref={props.annotationCanvasRef} width={props.imageMetadata.width} height={props.imageMetadata.height} ></canvas>
        {/* <h2>Hello</h2> */}

    </div>
    )


}


export default Canvas;