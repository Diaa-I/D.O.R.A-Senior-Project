import "./Modal.css"

export default function Modal (props){
    if(!props.isModalShown){
        return 
    }
    return(
        <>
<div className={"backdrop"} onClick={props.hideModal}></div>
<div className={"modal"}>
      <div>
        <h2>Feature yet to be added</h2>
        <p>This is feature is yet to be added, and will be added in the next patch</p>
        <buton onClick={props.hideModal} >Close</buton>
      </div>
</div>
</>

    )
}