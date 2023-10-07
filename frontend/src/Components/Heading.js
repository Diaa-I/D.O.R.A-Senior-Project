import './Heading.css'
import 'bootstrap/dist/css/bootstrap.css';
function Heading (){
    return(
    <>
        <div class="heading">
        <input class="form-control me-2 mb-4 custom" type="search" placeholder="Search" aria-label="Search" />
        <button class="add-project-button" data-bs-toggle = "modal" data-bs-target = "#project-modal">
        <span class="plus-sign">+ </span> Add New Project</button>
        </div>
    </>
    
)
}

export default Heading;