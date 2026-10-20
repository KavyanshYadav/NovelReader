
const THEMES = ["day","lamp","night"];
const savedTheme = localStorage.getItem("mt-theme");
if (savedTheme && THEMES.includes(savedTheme)) document.body.dataset.theme = savedTheme;
function setProgress(){
  const h=document.documentElement;
  const max=h.scrollHeight-h.clientHeight;
  document.getElementById("progress").style.width=(h.scrollTop/(max||1)*100)+"%";
}
addEventListener("scroll",setProgress,{passive:true}); setProgress();

document.getElementById("theme").onclick = () => {
  const order = THEMES;
  const next = order[(order.indexOf(document.body.dataset.theme)+1) % order.length];
  document.body.dataset.theme = next;
  localStorage.setItem("mt-theme", next);
};
document.getElementById("theme-hint").onclick =
  () => document.getElementById("theme").click();

document.getElementById("toc-toggle").onclick = () =>
  document.body.classList.toggle("n");
document.querySelectorAll(".toc-item").forEach(a =>
  a.addEventListener("click", () => document.body.classList.remove("n")));

const body=document.body;
function setFz(v){body.style.setProperty("--fz", v.toFixed(3)+"rem")}
let fz=1.035;
document.getElementById("fz-plus").onclick=()=>{fz=Math.min(1.6,fz+0.08); setFz(fz)};
document.getElementById("fz-minus").onclick=()=>{fz=Math.max(0.78,fz-0.08); setFz(fz)};

/* scrollspy: highlight the chapter whose heading is nearest above the fold */
const links=[...document.querySelectorAll(".toc-item")];
const targets=links.map(a=>document.getElementById(a.getAttribute("href").slice(1)));
const offsets=targets.map(t=>t?t.offsetTop:0);
function spy(){
  const y=scrollY + innerHeight*0.30;
  let i=0;
  for(let j=0;j<targets.length;j++) if(targets[j] && targets[j].offsetTop<=y) i=j;
  links.forEach((l,j)=>l.classList.toggle("active", j===i));
}
addEventListener("scroll",spy,{passive:true});
addEventListener("resize",spy,{passive:true});
addEventListener("load",spy);
spy();
/* keep the spy honest when the document height changes (font-size buttons) */
const spySync=setInterval(()=>links.forEach((l,j)=>{
  targets[j] && (offsets[j]=targets[j].offsetTop);
}),2000);

/* anchor navigation should land under the sticky bar */
links.forEach(a=>a.addEventListener("click",e=>{
  const id=a.getAttribute("href").slice(1);
  const t=document.getElementById(id);
  if(t){e.preventDefault(); history.replaceState(null,"","#"+id);
    scrollTo({top:t.offsetTop-72, behavior:"smooth"});}
}));
