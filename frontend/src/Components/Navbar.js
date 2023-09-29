import {Route,Routes,Link} from "react-router-dom"
import Workspace from "./Workspace"
import Test from "./Test"

export default function Navbar(props){
    return (
        <header>
        <div>
    <nav>

        <ul>
            <li><Link to='/test'>Home</Link></li>
            <li><Link to='/'>Workspace</Link></li>
            <li>Projects</li>
            <li>Datasets</li>
            <li>User</li>
        </ul>
    </nav>
    </div>
    <div>
     <Routes>
     <Route path='/' element={<Workspace showModal={props.showModal}  hideModal={props.hideModal}></Workspace>}/>
     <Route path='/test' element={<Test showModal={props.showModal}  hideModal={props.hideModal}></Test>}/>
   </Routes>
   </div>
   </header>
    )
}