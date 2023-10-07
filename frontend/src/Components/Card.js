import 'bootstrap/dist/css/bootstrap.css';
function Card(props){
    return(
    <div className="col-md-4">
      <div className="col">
              <div className="card">
              <svg className="bd-placeholder-img card-img-top" width="100%" height="225" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: Thumbnail" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#55595c"></rect><text x="50%" y="50%" fill="#eceeef" dy=".3em ">Project Cover</text></svg>
                  <div className="card-body">
                      <h5 className="card-title">{props.name}</h5>
                      <p className="card-text">Labels:{props.labels}</p>
                      <a href="#" className='btn btn-primary justify-content-end'>Open Project</a>
                  </div>
              </div>
          </div>
      </div>
    );
  }
  
  export default Card;