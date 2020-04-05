
//Speech Recognition
const SpeechRecognition=window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.continuous=true;
recognition.interimResults=false;

// recognition.lang='hi-IN';

document.querySelector('.cta-english').addEventListener('click',()=>{
    recognition.lang='en';

})
document.querySelector('.cta-bengali').addEventListener('click',()=>{
    recognition.lang='bn';

})
document.querySelector('.cta-hindi').addEventListener('click',()=>{
    recognition.lang='hi';

})
document.querySelector('.cta-marathi').addEventListener('click',()=>{
    recognition.lang='mr';

})
document.querySelector('.cta-telugu').addEventListener('click',()=>{
    recognition.lang='te';

})
document.querySelector('.cta-tamil').addEventListener('click',()=>{
    recognition.lang='ta';

})
document.querySelector('.cta-guj').addEventListener('click',()=>{
    recognition.lang='gu';

})
document.querySelector('.cta-hindi').addEventListener('click',()=>{
    recognition.lang='hi';

})
document.querySelector('.cta-hindi').addEventListener('click',()=>{
    recognition.lang='hi';

})
const addUserText=(text)=>{
    const userCharts=document.createElement("div");
    userCharts.classList.add('user-charts');
    const outgoingMsg=document.createElement("div");
    outgoingMsg.classList.add('outgoing-msg');
    const outgoingMsgInbox=document.createElement("div");
    outgoingMsgInbox.classList.add('outgoing-msg-inbox');
    const userContent=document.createElement("p");
   
    userContent.classList.add('user-content');
    const time=document.createElement('span');
    time.classList.add('time');
    time.classList.add('user');
    const userText = document.createTextNode(text);
 
    // console.log('userText='+userText); 
   
  
    userContent.appendChild(userText);
    userCharts.appendChild(outgoingMsg);
    outgoingMsg.appendChild(outgoingMsgInbox);
    let d = Date(Date.now()); 
     a = d.toString() 
    const sentTime=document.createTextNode(a);
    time.appendChild(sentTime);
    outgoingMsgInbox.appendChild(userContent);
    outgoingMsgInbox.appendChild(time);
    // console.log(userCharts);
  
   

    
    return userCharts;
}

const addBotText=(text)=>{
    const botCharts=document.createElement("div");
    botCharts.classList.add('bot-charts');
    const receivedMsg=document.createElement("div");
    receivedMsg.classList.add('received-msg');
    const receivedMsgInbox=document.createElement("div");
    receivedMsgInbox.classList.add('received-msg-inbox');
    const botContent=document.createElement("p");
    botContent.classList.add('bot-content');
    const time=document.createElement('span');
    time.classList.add('time');
    time.classList.add('bot');
    const botText = document.createTextNode(text);
    // console.log(botText);
    botContent.appendChild(botText);
    botCharts.appendChild(receivedMsg);
    receivedMsg.appendChild(receivedMsgInbox);
    let d = Date(Date.now()); 
     a = d.toString() 
    const sentTime=document.createTextNode(a);
    time.appendChild(sentTime);
    receivedMsgInbox.appendChild(botContent);
    receivedMsgInbox.appendChild(time);
    // console.log(botCharts);
    // console.log(botCharts.textContent);
    return botCharts;
    

}


async function translate(langCode,message){

     return  await $.post('/translate',{
        code:langCode,
        message:message
    }).done (function(data){
        data="";
     });
    // }).done(function(data){
    //     console.log(`Type===${typeof(data)}`);
    //     console.log(data);
    //     return data;

    // })
    // var translatedContent=document.createElement('div');
    // translatedContent.classList.add('generated');
    // console.log(translatedContent);

}





const BotVoice=async (message)=>{

    const Speech= new SpeechSynthesisUtterance();
    window.navigator.language=recognition.lang;
  
    // Speech.text=translate("Sorry!! Please Repeat",recognition.lang);
    // console.log(Speech.text);
    Speech.text= await translate(recognition.lang,message);
    


    Speech.volume=1;
    Speech.rate=1;
    Speech.pitch=1;
    window.speechSynthesis.speak(Speech);
    let element=document.querySelector('.msg-page');
    element.appendChild(addBotText(Speech.text));

    
}

recognition.onstart=()=>{
    console.log('Microphone Activated');
   

    swal({
        title: "Microphone Activated!",
        text: "You can start the chart!",
        icon: "success",
        button: "Ok",
      });
    // alert('Microphone Activated');
    
}

async function backTranslate(years,symptoms){

$.post('/back_translate',{
    years : 'years',
    symptoms : 'symptoms'
});
}
let data=[]

recognition.onresult=(event)=>{
  
    const current=event.resultIndex;
    const transcript=event.results[current][0].transcript;
    // console.log(transcript);
    // data.push(transcript)
    // console.log(`data=${data}`);
    // console.log('dataType='+typeof(data));
    
    // document.querySelector('.user-content').textContent=transcript;
    let element=document.querySelector('.msg-page');
    // console.log(element);
    element.appendChild(addUserText(transcript));
    
    BotVoice(transcript);

    let dataContent=document.querySelectorAll('.user');//this returns a node list
    let SymArray=Array.prototype.slice.call(dataContent);
    SymArray.forEach(cur=>{

    console.log('UserElement='+cur.previousElementSibling.textContent);
    let UserElement=cur.previousElementSibling.textContent;
    console.log(UserElement);
    if(recognition.lang=='hi-IN'){
    if(UserElement.includes('वर्षों')){
        document.getElementById('age').textContent=UserElement;
    }
    if(UserElement.includes('लक्षण')){
      
        document.getElementById('symptomsPatient').value=UserElement;
        
    }
    if(UserElement.includes('हाँ')||UserElement.includes('हां')){
        document.querySelector('.input-group').style.display='block';
    }
    }

    if(recognition.lang=='en'){
    if(UserElement.includes('years')){
        document.getElementById('age').textContent=UserElement;
    }
    if(UserElement.includes('symptoms')||UserElement.includes('suffering')){
      
        document.getElementById('symptomsPatient').value=UserElement;
        
    }
    if(UserElement.includes('yes')){
        document.querySelector('.input-group').style.display='block';
    }
    }

    if(recognition.lang=='bn'){
    if(UserElement.includes('বছর')){
        document.getElementById('age').textContent=UserElement;
    }
    if(UserElement.includes('বছর')){
      
        document.getElementById('symptomsPatient').value=UserElement;
        
    }
    if(UserElement.includes('হ্যাঁ')){
        document.querySelector('.input-group').style.display='block';
    }
    }

    if(recognition.lang=='te'){
    if(UserElement.includes('సంవత్సరాల')){
        document.getElementById('age').textContent=UserElement;
    }
    if(UserElement.includes('సంవత్సరాల')){
      
        document.getElementById('symptomsPatient').value=UserElement;
        
    }
    if(UserElement.includes('అవును')){
        document.querySelector('.input-group').style.display='block';
    }
    }

    if(recognition.lang=='ta'){
    if(UserElement.includes('ஆண்டுகள்')){
        document.getElementById('age').textContent=UserElement;
    }
    if(UserElement.includes('அறிகுறிகள்')){
      
        document.getElementById('symptomsPatient').value=UserElement;
        
    }
    if(UserElement.includes('ஆம்')){
        document.querySelector('.input-group').style.display='block';
    }
    }
    
   if(recognition.lang=='mr'){
    if(UserElement.includes('वर्षे')){
        document.getElementById('age').textContent=UserElement;
    }
    if(UserElement.includes('लक्षणे')){
      
        document.getElementById('symptomsPatient').value=UserElement;
        
    }
    if(UserElement.includes('होय')){
        document.querySelector('.input-group').style.display='block';
    }
    }

    if(recognition.lang=='gu'){
    if(UserElement.includes('વર્ષો')){
        document.getElementById('age').textContent=UserElement;
    }
    if(UserElement.includes('લક્ષણો')){
      
        document.getElementById('symptomsPatient').value=UserElement;
        
    }
    if(UserElement.includes('હા')){
        document.querySelector('.input-group').style.display='block';
    }
    }

})

  

}





document.querySelector('.mic').addEventListener('click',()=>{
    recognition.start();
})

document.querySelector('.mic-stop').addEventListener('click',()=>{
    recognition.abort();
    // alert("Microphone Deactivated");
    swal({
        title:"Microphone Deactivated"
    })
    
})

document.querySelector('.mic-chat').addEventListener('click',()=>{
    document.querySelector('.cover-chat').style.display="block";
})






