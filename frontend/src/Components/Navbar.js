import React, { useState } from 'react';
import { Routes, Route, Link, NavLink } from 'react-router-dom';
import Workspace from './workspace/Workspace';
import Test from './Test';
import Projects from './project/Projects';
import Datasets from './dataset/Datasets';
import 'bootstrap/dist/css/bootstrap.css';
import './Navbar.css';
import { FaBars, FaArrowLeft, FaHome, FaBriefcase, FaProjectDiagram, FaDatabase, FaUser } from 'react-icons/fa';

      
export default function Navbar(props){
    useState(flase)
    return(
<div>
<div class="tab-container">
    <div class="tab-nav">
        <img class ="logo" src="../public/images/logo-D-org.png" />
        <nav>
        <ul>
            <li>
                <FaHome  className='icon'/>
                <Link to='/test' className='custom'>Home</Link>
            </li>
            <li>
                <FaBriefcase className='icon'/>
                <Link to='/' className='custom'>Workspace</Link>
            </li>
            <li>
                <FaProjectDiagram className='icon'/>
                <Link to='/Projects' className='custom'>Projects</Link>
            </li>

            <li>
                <FaDatabase className='icon'/>
                <Link to='/Datasets' className='custom'>Datasets</Link>
            </li>
            <li>
                <FaUser className='user-icon'/>
            </li>

        </ul>

        </nav>
        
        
    </div>
         
</div>

    <div>
     <Routes>
     <Route path='/' element={<Workspace showModal={props.showModal}  hideModal={props.hideModal}></Workspace>}/>
     <Route path='/test' element={<Test showModal={props.showModal}  hideModal={props.hideModal}></Test>}/>
     <Route path='/Projects' element={<Projects showModal={props.showModal}  hideModal={props.hideModal}></Projects>}/>
     <Route path='/Datasets' element={<Datasets showModal={props.showModal}  hideModal={props.hideModal}></Datasets>}/>
   </Routes>
   </div>
   </div>
    );
}
   