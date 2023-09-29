import "./Modal.css"

export default function Modal (props){
    console.log("11111111111111111111111111111212")
    // console.log(classes.backdrop)
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
        // <div class="modal" id="modal" onClick={props.hideModal} >
        //    <h2> Hello Modal </h2>
        //    <div class="actions">
        //   <button class="toggle-button" onClick={props.hideModal} >
        //     close
        //   </button>
        // </div>
        // </div>
    )
}