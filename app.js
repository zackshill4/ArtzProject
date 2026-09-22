const form=document.querySelector("#command-form");
const input=document.querySelector("#command-input");
const terminal=document.querySelector("#terminal");
const clock=document.querySelector("#clock");

function tick(){clock.textContent=new Date().toLocaleTimeString("en-GB",{hour12:false})}
tick();setInterval(tick,1000);

const commands={
help:[
 "AVAILABLE COMMANDS:",
 "  1          system info",
 "  2          SHA-256 file hash",
 "  3 <text>   Base64 encode",
 "  3d <text>  Base64 decode",
 "  4 <json>   JSON formatter",
 "  status     display ARTZ system status",
 "  profile    show protagonist profile",
 "  world      show current world state",
 "  clear      clear terminal"
],
status:["ARTZ CORE ........ ONLINE","VOID SYNC ........ 87%","NETWORK .......... STABLE","THREAT ........... ELEVATED"],
profile:["NAME ............. ARTZ","CLASS ............ VOID WARDEN","LEVEL ............ 27","STATUS ........... ACTIVE"],
world:["REGION ........... NOCTIS","QUESTS ........... 04 ACTIVE","GATE STATUS ...... CORRUPTED","OBJECTIVE ........ THE VEIL IS OPEN"]
};

function print(text,cls="line"){
 const line=document.createElement("div");
 line.className=cls;
 line.innerHTML=text;
 terminal.appendChild(line);
}

async function sha256File(){
 const picker=document.createElement("input");
 picker.type="file";
 picker.style.display="none";
 document.body.appendChild(picker);
 picker.addEventListener("change",async()=>{
   const file=picker.files[0];
   if(!file){picker.remove();return}
   try{
     const buffer=await file.arrayBuffer();
     const hash=await crypto.subtle.digest("SHA-256",buffer);
     const hex=[...new Uint8Array(hash)].map(b=>b.toString(16).padStart(2,"0")).join("");
     print("FILE ............ "+escapeHtml(file.name));
     print("SHA-256 ......... "+hex,"line accent");
   }catch(err){print("HASH ERROR ....... "+escapeHtml(err.message))}
   picker.remove();
   terminal.scrollTop=terminal.scrollHeight;
 });
 picker.click();
}

function systemInfo(){
 const info=[
  "SYSTEM ........... "+escapeHtml(navigator.platform||"WEB"),
  "BROWSER .......... "+escapeHtml(navigator.userAgent),
  "LANGUAGE ......... "+escapeHtml(navigator.language),
  "CORES ............ "+(navigator.hardwareConcurrency||"N/A"),
  "MEMORY ........... "+(navigator.deviceMemory?navigator.deviceMemory+" GB":"N/A"),
  "ONLINE ........... "+(navigator.onLine?"YES":"NO")
 ];
 info.forEach((x,i)=>print(x,i===0?"line accent":"line"));
}

function base64Command(raw){
 const value=raw.slice(1).trim();
 if(!value){print("USAGE ............ 3 <text> OR 3d <base64>","line accent");return}
 try{
   if(raw.toLowerCase().startsWith("3d")){
     const data=raw.slice(2).trim();
     print("DECODED .......... "+escapeHtml(atob(data)),"line accent");
   }else{
     print("ENCODED .......... "+btoa(unescape(encodeURIComponent(value))),"line accent");
   }
 }catch(err){print("BASE64 ERROR ...... INVALID INPUT")}
}

function jsonCommand(raw){
 const value=raw.slice(1).trim();
 if(!value){print("USAGE ............ 4 <json>","line accent");return}
 try{print(escapeHtml(JSON.stringify(JSON.parse(value),null,2)).replace(/\n/g,"<br>"),"line accent")}
 catch(err){print("JSON ERROR ........ INVALID JSON")}
}

form.addEventListener("submit",async e=>{
 e.preventDefault();
 const raw=input.value.trim();
 const cmd=raw.toLowerCase();
 if(!raw)return;
 print('<span class="dim">&gt; '+escapeHtml(raw)+'</span>');
 if(cmd==="clear"){terminal.innerHTML="";input.value="";return}
 if(cmd==="1"){systemInfo()}
 else if(cmd==="2"){print("SELECT FILE ........ waiting for file picker","line dim");await sha256File()}
 else if(cmd.startsWith("3d ")||cmd==="3d"){base64Command(raw)}
 else if(cmd.startsWith("3 ")||cmd==="3"){base64Command(raw)}
 else if(cmd.startsWith("4 ")||cmd==="4"){jsonCommand(raw)}
 else{
   const key=cmd.split(/\s+/)[0];
   (commands[key]||["UNKNOWN COMMAND.","Type <b>help</b> for available commands."]).forEach((text,i)=>print(text,i===0&&commands[key]?"line accent":"line"));
 }
 terminal.scrollTop=terminal.scrollHeight;
 input.value="";
});

function escapeHtml(s){
 return s.replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
}
