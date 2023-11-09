import React, { useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Workspace from './workspace/Workspace';
import Test from './Test';
import Projects from './project/Projects';
import Datasets from './dataset/Datasets';
// import Models from './Models/Models'
import 'bootstrap/dist/css/bootstrap.css';
import './Navbar.css';
import logo from '../images/logo.png';

export default function Navbar(props) {
  // Create state to track whether the sidebar is open or closed
  const [isSidebarOpen, setSidebarOpen] = useState(true);

  // Function to toggle the sidebar
  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className='contianer'>
      <nav className={`sidebar ${isSidebarOpen ? 'open' : 'close'}`}>
        <header>
          <div className="image-text">
            <span className="image">
              <img src={logo} alt="logo" />
            </span>

            <div className="text logo-text">
              <span className="name">DORA</span>
            </div>
          </div>

          <i className={`bx ${isSidebarOpen ? 'bx-chevron-right' : 'bx-chevron-left'} toggle`} onClick={toggleSidebar}></i>
        </header>

        <div className="menu-bar">
            <div className="menu">

                <ul className="menu-links">
                    <li className="nav-link">
                        <Link to="/">
                            <i className='bx bx-outline icon'></i>
                            <span className="text nav-text">Home</span>
                        </Link>
                    </li>

                    <li className="nav-link">
                        <Link to="/Datasets">
                            <i className='bx bx-data icon'></i>
                            <span className="text nav-text">Datasets</span>
                        </Link>
                    </li>

                    <li className="nav-link">
                        <Link to="/Models">
                            <i className='bx bx-shape-circle icon'></i>
                            <span className="text nav-text">Models</span>
                        </Link>
                    </li>

                    <li className="nav-link">
                        <Link to="/Projects">
                            <i className='bx bxs-collection icon'></i>
                            <span className="text nav-text">Projects</span>
                        </Link>
                    </li>    

                </ul>
            </div>

            <div className="bottom-content">
                <li className="">
                    <a href="#">
                        <i className='bx bxs-user icon'></i>
                        <span className="text nav-text">User Account</span>
                    </a>
                </li>
                <li>
                    <a href="'#">
                        <i className='bx bx-cog icon' ></i>
                        <span className="text nav-text">Settings</span>
                    </a>
                    
                </li>
                
            </div>
        </div>

    </nav>
        
    <div className='content'>
     <Routes>
     <Route path='/workspace/:id' element={<Workspace showModal={props.showModal}  hideModal={props.hideModal}></Workspace>}/>
     <Route path='/' element={<Test showModal={props.showModal}  hideModal={props.hideModal}></Test>}/>
     <Route path='/Projects' element={<Projects showModal={props.showModal}  hideModal={props.hideModal}></Projects>}/>
     <Route path='/Datasets' element={<Datasets showModal={props.showModal}  hideModal={props.hideModal}></Datasets>}/>
     {/* <Route path='/Models' element={<Models showModal={props.showModal}  hideModal={props.hideModal}></Models>}/> */}

   </Routes>
   </div>
   </div>
    );
}
   