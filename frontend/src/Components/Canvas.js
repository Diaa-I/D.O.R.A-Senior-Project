import './workspace.css'
import {useRef,useEffect} from "react"

const Canvas = (props) => {

    const Annotations = props.Annotations;
    console.log(props.forwardRef)

   


    return(
    <div className="canvas" >
        <p>
            {Annotations.map(el=><ul><li>x:{el.x}</li><li>y:{el.y}</li><li>w:{el.width}</li><li>h:{el.height}</li><li>h:{el.color}</li><li>{el.label}</li></ul>)}
        </p>
        {/* When annotations then get printed here */}
        {/* And we loop onclick we can call a function when that happens the values in the rectangle should change */}
        <canvas className="canvas-body" itemID="canvas" ref={props.forwardRef} ></canvas>
    </div>
    )


}


export default Canvas;