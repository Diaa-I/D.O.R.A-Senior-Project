import 'bootstrap/dist/css/bootstrap.css';

function  SearchBar({projects}){
    console.log(projects)
    
    return(
          <input class="form-control me-2 mb-3" type="search" placeholder="Search" aria-label="Search" style = {{width: '35vw'}}/>
        );
}

export default SearchBar; 