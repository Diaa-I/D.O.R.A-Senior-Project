import React from 'react';
import { Modal, Spinner } from 'react-bootstrap';

function LoadingModal(props) {
  return (
    <Modal show={props.isLoading} centered backdrop= 'static' style={{background: 'rgba(255, 255, 255, 0.8)', backdropFilter: 'blur(5px)' }}>
        <Modal.Title className='text-center mt-3'>Page Loading</Modal.Title> 
            <Modal.Body>
                <div className="text-center">
                <Spinner animation="border" role="status" variant='primary'>
                </Spinner>
                <h6 className="sr-only mt-3">Loading...</h6>

            </div>
      </Modal.Body>
    
    </Modal>
  );
}

export default LoadingModal;
