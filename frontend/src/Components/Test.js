import axios from "axios"
import { useEffect, useState } from "react"

export default function Test(props){

    const [loading,setLoading] = useState(true)
    const [item,setItem] = useState(false)

    useEffect(()=>{
        axios.get("http://localhost:5000/a").then(res=>{
            setItem(res.data)
            setLoading(false)
        })
    },[])
    if (loading) {
        return <div className="App">Loading...</div>;
      }
    
      return (
        <div className="App">
          <h1>{item.Project_Name}</h1>
          <h2>{item.Frames}</h2>
          {/* <img alt={item.name} src={item.sprites.front_default} /> */}
        </div>
      );
}