const express=require("express")
const app=express()
const path=require('path')
const mongoose=require("mongoose")
const methodOverride=require("method-override")
const session=require("express-session")
const flash=require("connect-flash")

app.set('view engine','ejs')
app.set('views',path.join(__dirname,'views'))
app.use(express.urlencoded({extended:true}))
app.use(methodOverride("_method"))

app.use(express.static(path.join(__dirname, '/public/')))

const sessionConfig={
    secret:"thisisagoodsecret",resave:false,saveUninitialized:false,
    cookie:{ 
    httpOnly:true,
    expires:Date.now()+1000*60*60*24*7,
    maxAge:1000*60*60*24*7
    },
}
app.use(session(sessionConfig))
app.use(flash())

app.use((req,res,next)=>{
    
    res.locals.currentUser=req.user
    res.locals.created=req.flash("created")    
    res.locals.updated=req.flash("updated")    
    res.locals.deleted=req.flash("deleted")    
    res.locals.error=req.flash("error")    
    next()
    })

mongoose.connect("mongodb://127.0.0.1:27017/DORA", {useNewUrlParser: true, useUnifiedTopology: true})
.then(()=>{
console.log("YOYOYO")    
})
.catch( e=>{
console.log(`error is ${e}`)
}) 



app.listen(8080,()=>{
    console.log("Listening on port 8080")    
})