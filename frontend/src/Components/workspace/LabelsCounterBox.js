
export default function LabelsCounterBox(props){
console.log("HELLELEE")
console.log(props.labelsCounter)
const labelsObj = [] 
for(let label in props.labelsCounter){
    labelsObj.push(<li>{label}{props.labelsCounter[label]}</li>)
}
labelsObj.map((element)=>{console.log(element.props.children)})
return (
    <div className="a">
    <ul>
    {labelsObj.map((element)=>{return element.props.children})}
    </ul>
    </div>
);
}