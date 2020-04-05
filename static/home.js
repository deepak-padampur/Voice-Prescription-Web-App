const theme=document.querySelector('.theme');
const slider=document.querySelector('.slider');
const logo=document.querySelector('#logo');
const hamburger=document.querySelector('.hamburger');
const headline=document.querySelector('.headline');


const t1=new TimelineMax();

t1.fromTo(theme,2,{
    height:"0%"
},{height:"90%",ease:Power2.easeInOut})
.fromTo(theme,1.2,{width:"100%"},{width:"80%",ease:Power2.easeInOut})
.fromTo(slider,1.2,{x:"-100%"},{x:'0%',ease:Power2.easeInOut},"-=1.2")
.fromTo(logo,0.5,{opacity:0,x:30},{opacity:1,x:0},"-=0.5")
.fromTo(hamburger,0.5,{opacity:0,x:30},{opacity:1,x:0},"-=1")

const hamburderLines=document.querySelectorAll('.menu line');
const navOpen=document.querySelector('.nav-open');
const doctor=document.querySelector('.doctor');
const pages=document.querySelector('.pages');


const tl=new TimelineMax({paused:true,reversed:true});
tl.to(navOpen,0.5,{y:0})
.fromTo(doctor,0.5,{opacity:0,y:10},{opacity:1,y:0},"-=0.1")
.fromTo(pages,0.5,{opacity:0,y:10},{opacity:1,y:0},"-=0.5")
.fromTo(logo,0.2,{color:'white'},{color:'black'},"-=1")


hamburger.addEventListener('click',()=>{
    console.log('clicked');
    tl.reversed()?tl.play():tl.reverse();
});



