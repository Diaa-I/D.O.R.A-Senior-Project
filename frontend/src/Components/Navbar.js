import {Route,Routes,Link} from "react-router-dom"
import Workspace from "./workspace/Workspace"
import Test from "./Test"
import Project_Modal from "./project/Project_Modal"

export default function Navbar(props){
    return (
        <header>
        <div>
    <nav>

        <ul>
            <li><Link to='/test'>Home</Link></li>
            <li><Link to='/'>Workspace</Link></li>
            <li><Link to='/Projects'>Projects</Link></li>
            <li><Link to='/Datasets'>Datasets</Link></li>
            <li>User</li>
        </ul>
    </nav>
    </div>
    <div>
     <Routes>
     <Route path='/' element={<Workspace showModal={props.showModal}  hideModal={props.hideModal}></Workspace>}/>
     <Route path='/test' element={<Test showModal={props.showModal}  hideModal={props.hideModal}></Test>}/>
     {/* <Route path='/Projects' element={<Project_Modal showModal={props.showModal}  hideModal={props.hideModal}></Project_Modal>}/> */}
     {/* <Route path='/Datasets' element={<Test showModal={props.showModal}  hideModal={props.hideModal}></Test>}/> */}
   </Routes>
   </div>
   </header>
    )
}