import axios from "axios"
import { useEffect, useState } from "react"

export default function Test(props){
    // const [loading,setLoading] = useState(true)
    // const [item,setItem] = useState(false)
    // const [image,setImage] = useState('')
    useEffect(()=>{
      let annotatedFrames = []
      for (let i=0;i<=50;i++){
        annotatedFrames.push(i)
    }


        axios.post("http://localhost:5000/",{"annotatedFrames":annotatedFrames} ).then(res=>{
          console.log(res.data)
        }).catch((err)=>console.log(err))
    },[])
    // if (loading) {
    //     return <div className="App">Loading...</div>;
    //   }
    
      return (
        <div className="App">
          {/* <h1>{item.Project_Name}</h1>
          <h2>{item.Frames}</h2>
          <img src={process.env.PUBLIC_URL+image} width={'500px'}></img> */}
        </div>
      );
}