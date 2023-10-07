import axios from "axios"
import { useEffect, useState } from "react"

export default function Test(props){
    const [loading,setLoading] = useState(true)
    const [item,setItem] = useState(false)
    const [image,setImage] = useState('')
    useEffect(()=>{
        axios.get("http://localhost:5000/workspace/retrieve_next_batch?starting_from=0&retrieval_size=1").then(res=>{
            setItem(res.data)
            setImage(res.data['Image_Dir'])
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
          <img src={process.env.PUBLIC_URL+image} width={'500px'}></img>
        </div>
      );
}