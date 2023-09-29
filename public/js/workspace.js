//ADD ANother canvas on the front that will be transparent and used for the annotation




const canvas = document.querySelector("#canvas")
let canvasContext = canvas.getContext("2d")
const btn = document.querySelector(".square")
let isDragging = false;
let current_shape_index = 0;
let startX;
let startY;
let offset_x;
let offset_y;
let shapes = []
shapes.push({x:200 ,y:50, width:200, height: 200, color:"red"}) 



let get_offset = function() {
    let canvas_offsets = canvas.getBoundingClientRect();
    offset_x = canvas_offsets.left;
    offset_y = canvas_offsets.top;
    console.log(offset_x,offset_y)
}
get_offset()
window.onresize = function(){get_offset()}
canvas.onresize = function(){get_offset()}
canvas.onscroll = function(){get_offset()}
let draw_shapes = function(){
    canvasContext.clearRect(0,0,canvas.width,canvas.height)
    for(let shape of shapes){
        canvasContext.fillStyle = shape.color
        canvasContext.fillRect(shape.x,shape.y,shape.width,shape.height)
        return;
    }   
}

let is_mouse_in_shape = function(x,y,shape){
    let shape_left = shape.x
    let shape_right = shape.x + shape.width
    let shape_top = shape.y
    let shape_bottom = shape.y + shape.height
    console.log(x,y)
    console.log(shape_left,shape_right,shape_top,shape_bottom)
    if(x > shape_left && x < shape_right && y > shape_top && y < shape_bottom )
    {
        return true
    }
    return false
}

btn.addEventListener("click",(doc)=>{
   draw_shapes()
})
// mouse down
let mouse_down = function(event){
    event.preventDefault()
    startX = parseInt(event.clientX - offset_x)
    startY = parseInt(event.clientY- offset_y)
    console.log(startX,startY)
    let i = 0
    for(let shape of shapes){
        if(is_mouse_in_shape(startX,startY,shape)){
            current_shape_index = i
            isDragging = true
            return;
        }
        i++
    }

}

// mouse up 
let mouse_up = function(event){
    event.preventDefault()
    if(!isDragging){
        return ; 
    }
    isDragging = false
}

// out of canvas
let mouse_out = function(event){
    if(!isDragging){
        return ; 
    }
    event.preventDefault()
    isDragging = false
}

// Drag and drop
let mouse_move = function(event) {
    if(!isDragging){
        return ; 
    }
    else {
    event.preventDefault()
    let mouseX = parseInt(event.clientX - offset_x)
    let mouseY = parseInt(event.clientY - offset_y)
    let dx = mouseX - startX
    let dy = mouseY - startY
    let current_shape = shapes[current_shape_index]
    current_shape.x = dx
    current_shape.y = dy
    draw_shapes()
    startX = mouseX
    startY = mouseY
}
}
canvas.onmousedown = mouse_down
canvas.onmouseup = mouse_up
canvas.onmouseout = mouse_out
canvas.onmousemove = mouse_move

