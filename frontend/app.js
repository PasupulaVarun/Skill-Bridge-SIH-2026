const state = {
  role: localStorage.getItem("sb_role") || "student",
  page: localStorage.getItem("sb_page") || "dashboard",
  assessmentDone: localStorage.getItem("sb_assessment") === "1",
  applied: JSON.parse(localStorage.getItem("sb_applied") || "[]")
};

const data = {
  student: {
    name:"Varun", eyebrow:"STUDENT PORTAL", title:"Your career command center",
    nav:[
      ["dashboard","⌂","Dashboard"],["assessment","✓","Skill Assessment"],["skills","◈","Skill Profile"],
      ["opportunities","⌁","Opportunities"],["applications","◷","Applications"],["learning","✦","Learning"],
      ["portfolio","▣","Portfolio"]
    ]
  },
  industry: {
    name:"Industry", eyebrow:"INDUSTRY PORTAL", title:"Find the right talent faster",
    nav:[
      ["dashboard","⌂","Dashboard"],["post","＋","Post Opportunity"],["candidates","◎","Candidate Matches"],
      ["industryApps","◷","Applications"],["mentorship","✦","Mentorship"]
    ]
  },
  institution: {
    name:"Institution", eyebrow:"INSTITUTION PORTAL", title:"Monitor readiness and outcomes",
    nav:[
      ["dashboard","⌂","Dashboard"],["students","◎","Students"],["analytics","▥","Analytics"],
      ["programs","▣","Programs"],["reports","⇩","Reports"]
    ]
  },
  academician: {
    name:"Academician", eyebrow:"ACADEMICIAN PORTAL", title:"Connect academia with industry",
    nav:[
      ["dashboard","⌂","Dashboard"],["facultyOps","⌁","Faculty Opportunities"],["fdp","✦","FDPs"],
      ["research","◇","Research"],["collaboration","◎","Collaboration"]
    ]
  }
};

const opportunities = [
  {id:1,title:"Backend Developer Intern",company:"TechNova Labs",type:"Internship",location:"Remote",duration:"8 weeks",skills:["Python","SQL","REST API","Docker"],match:84,why:"Python + SQL strength; backend target aligned. Docker is the main manageable gap."},
  {id:2,title:"Data Engineering Intern",company:"Aster Analytics",type:"Internship",location:"Hybrid • Bengaluru",duration:"12 weeks",skills:["Python","SQL","ETL","Cloud"],match:78,why:"Strong Python/SQL foundation; ETL and cloud are next-step skills."},
  {id:3,title:"Junior API Developer",company:"MedTech Systems",type:"Entry-level",location:"Hyderabad",duration:"Full-time",skills:["Python","FastAPI","PostgreSQL","Git"],match:76,why:"Backend pathway fit with strong Python; FastAPI and PostgreSQL deepen the stack."},
  {id:4,title:"AI/ML Project Trainee",company:"Innova Research",type:"Live Project",location:"Remote",duration:"6 weeks",skills:["Python","ML","Pandas","Scikit-learn"],match:69,why:"Good Python base; project adds practical ML evidence to your portfolio."}
];

function save(){localStorage.setItem("sb_role",state.role);localStorage.setItem("sb_page",state.page);localStorage.setItem("sb_assessment",state.assessmentDone?"1":"0");localStorage.setItem("sb_applied",JSON.stringify(state.applied))}
function toast(msg){const t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2600)}
function setPage(page){state.page=page;save();render()}
function setRole(role){state.role=role;state.page="dashboard";save();render()}

function navHTML(){
  return data[state.role].nav.map(n=>`<button class="nav-item ${state.page===n[0]?'active':''}" onclick="setPage('${n[0]}')"><span class="nav-icon">${n[1]}</span>${n[2]}</button>`).join("");
}

function statCard(icon,label,value,delta){return `<div class="card stat"><div><div class="muted small">${label}</div><div class="value">${value}</div><div class="delta">${delta}</div></div><div class="stat-icon">${icon}</div></div>`}

function studentDashboard(){
 return `
 <div class="hero">
   <div class="eyebrow" style="color:#7fe1d2">SMART CAREER PIPELINE</div>
   <h2>Measure → improve → connect → apply → grow.</h2>
   <p>Your skills, learning actions, internships and portfolio in one intelligent workflow. The demo uses explainable matching rather than an opaque AI score.</p>
   <button class="btn light" onclick="setPage('assessment')">${state.assessmentDone?'Review assessment':'Start 5-minute assessment'} →</button>
 </div>
 <div class="grid grid-4" style="margin-top:18px">
   ${statCard("◉","Skill readiness",state.assessmentDone?"78%":"—",state.assessmentDone?"+12% this month":"Take assessment")}
   ${statCard("⌁","Top opportunity match","84%","4 new matches")}
   ${statCard("✦","Priority skill gaps","2","Docker • API testing")}
   ${statCard("◷","Applications","2","1 shortlisted")}
 </div>
 <div class="section-head"><h2>What needs your attention?</h2><button class="link-btn" onclick="setPage('skills')">View skill profile →</button></div>
 <div class="grid grid-2">
   <div class="card">
     <div class="profile-row"><div class="profile-photo">VP</div><div><strong>Varun Pasupula</strong><div class="muted small">CSE • Year 1 • Target: Backend Developer</div></div><span class="badge-verified" style="margin-left:auto">✓ Profile 92%</span></div>
     <div style="margin-top:22px">
       ${skill("Python",95)}${skill("SQL",88)}${skill("Git",80)}${skill("REST APIs",58)}
     </div>
   </div>
   <div class="card"><h3>Priority skill gaps</h3>
     ${gap("Docker",4,2,"Complete containerization mini-project")}
     ${gap("API Testing",4,2,"Learn Postman + write 5 API tests")}
     <button class="btn" style="margin-top:10px" onclick="setPage('learning')">Open action plan</button>
   </div>
 </div>
 <div class="section-head"><h2>Recommended opportunities</h2><button class="link-btn" onclick="setPage('opportunities')">Explore all →</button></div>
 <div class="grid grid-2">
   <div class="card">${opportunities.slice(0,3).map(opCard).join("")}</div>
   <div class="card"><h3>Application progress</h3><div class="timeline" style="margin-top:18px">
     ${step("Assessment complete","Skill profile generated",true)}
     ${step("Opportunity selected","2 applications submitted",true)}
     ${step("Shortlisted","TechNova Labs • Backend Intern",true)}
     ${step("Interview","Prepare portfolio + API project",false)}
   </div></div>
 </div>`;
}
function skill(name,val){return `<div class="skill-row"><div class="skill-meta"><strong>${name}</strong><span>${val}/100</span></div><div class="progress"><span style="width:${val}%"></span></div></div>`}
function gap(name,req,current,action){let g=req-current;return `<div class="gap-card" style="margin-top:11px"><div class="gap-top"><strong>${name}</strong><span class="gap-size">Gap ${g}</span></div><div class="muted small">Required level ${req}/5 • Current level ${current}/5</div><div class="reason">→ ${action}</div></div>`}
function step(title,sub,done){return `<div class="step ${done?'done':''}"><div class="step-dot"></div><div><div class="step-title">${title}</div><div class="step-sub">${sub}</div></div></div>`}
function opCard(op){
 const applied=state.applied.includes(op.id);
 return `<div class="match-card"><div><div class="company">${op.title}</div><div class="muted small">${op.company} • ${op.type}</div><div class="reason">${op.why}</div><div>${op.skills.map(s=>`<span class="pill">${s}</span>`).join("")}</div></div><div style="text-align:right"><div class="match">${op.match}%</div><div class="muted small">match</div><div class="match-actions"><button class="btn ${applied?'outline':''}" onclick="applyOpportunity(${op.id})" ${applied?'disabled':''}>${applied?'Applied':'Apply'}</button></div></div></div>`;
}
function applyOpportunity(id){if(!state.applied.includes(id)){state.applied.push(id);save();toast("Application submitted. Status: Applied");render()}}

function assessment(){
 const qs=[
 ["Which approach is best for a reusable backend service?","Python + FastAPI with clear API contracts","Only client-side JavaScript","A single giant HTML file"],
 ["What does a SQL JOIN primarily do?","Combines related rows across tables","Encrypts a database","Compiles Python"],
 ["Which is a useful reason to use Docker?","Consistent application environments","Replacing source control","Automatically guaranteeing security"],
 ["A good API test should verify…","Expected request/response behavior and edge cases","Only the page color","That the developer likes the endpoint"],
 ["When receiving critical feedback, the strongest response is…","Understand it, act on it, and verify improvement","Ignore it","Avoid future feedback"]
 ];
 return `<div class="grid grid-2"><div class="card"><div class="eyebrow">5-MINUTE ASSESSMENT</div><h2 style="margin:4px 0 8px">Baseline your practical skills</h2><p class="muted small">Questions are illustrative for the prototype. In production, each question maps to normalized skill IDs and measurable competency levels.</p>
 ${qs.map((q,i)=>`<div class="question"><p>${i+1}. ${q[0]}</p>${q.slice(1).map((a,j)=>`<label class="option"><input type="radio" name="q${i}" value="${j===0?1:0}"> ${a}</label>`).join("")}</div>`).join("")}
 <button class="btn" onclick="finishAssessment()">Submit assessment</button></div>
 <div class="card"><h3>What happens next?</h3><div class="feature-list">
 <div>✓ <span><b>Profile</b> — convert responses into skill-level estimates.</span></div>
 <div>✓ <span><b>Gap analysis</b> — compare current level with target-role requirements.</span></div>
 <div>✓ <span><b>Action plan</b> — map gaps to learning, projects and mentors.</span></div>
 <div>✓ <span><b>Matching</b> — rank opportunities with visible reasons.</span></div></div>
 <div style="margin-top:24px" class="card" style="box-shadow:none"><div class="muted small">Current target role</div><strong style="font-size:20px">Backend Developer</strong><div class="muted small" style="margin-top:5px">Python • SQL • APIs • Cloud fundamentals</div></div>
 </div></div>`;
}
function finishAssessment(){state.assessmentDone=true;save();toast("Assessment complete — your skill profile is ready.");setPage("skills")}

function skillsPage(){return `<div class="grid grid-2">
 <div class="card"><div class="eyebrow">SKILL PROFILE</div><h2 style="margin:3px 0 18px">Your current capability map</h2>${skill("Python",95)}${skill("SQL",88)}${skill("Git",80)}${skill("REST APIs",58)}${skill("Docker",42)}${skill("API Testing",38)}${skill("Communication",82)}${skill("Problem Solving",86)}</div>
 <div class="card"><h3>Target-role gap analysis</h3><p class="muted small">Backend Developer • required levels are illustrative.</p>${gap("Docker",4,2,"Containerize your API project")}${gap("API Testing",4,2,"Create a Postman test collection")}${gap("REST APIs",4,3,"Build authentication + validation")}</div>
 </div>
 <div class="section-head"><h2>Gap → action</h2></div>
 <div class="grid grid-3">${learningCard("Docker Foundations","Tech Academy","4 weeks","Docker")}${learningCard("API Testing with Postman","Open Learning Lab","2 weeks","API Testing")}${learningCard("Build a Production REST API","SkillBridge Project","3 weeks","REST APIs")}</div>`}
function learningCard(t,p,d,s){return `<div class="card"><span class="pill amber">${s}</span><h3 style="margin-top:10px">${t}</h3><div class="muted small" style="margin-top:5px">${p} • ${d}</div><button class="btn outline" style="margin-top:15px" onclick="toast('Learning program saved to your action plan')">Add to plan</button></div>`}

function opportunitiesPage(){return `<div class="card"><div class="searchbar"><input id="opSearch" placeholder="Search internships, jobs, skills or companies…" oninput="filterOps()"><button class="btn" onclick="toast('Filters ready')">Filter</button></div><div class="filters"><span class="pill green">Recommended for you</span><span class="pill">Internship</span><span class="pill">Remote</span><span class="pill">Entry-level</span></div><div id="opList">${opportunities.map(op=>`<div data-search="${(op.title+' '+op.company+' '+op.skills.join(' ')).toLowerCase()}">${opCard(op)}</div>`).join("")}</div></div>`}
function filterOps(){let q=document.getElementById("opSearch").value.toLowerCase();document.querySelectorAll("#opList>[data-search]").forEach(x=>x.style.display=x.dataset.search.includes(q)?"block":"none")}

function applications(){return `<div class="card"><div class="section-head" style="margin-top:0"><h2>Application tracker</h2><span class="pill green">${state.applied.length} active</span></div>
 ${state.applied.length?state.applied.map(id=>{let o=opportunities.find(x=>x.id===id);return `<div class="opportunity"><div class="op-head"><div><div class="op-title">${o.title}</div><div class="op-company">${o.company}</div></div><span class="badge-verified">Applied</span></div><div class="timeline" style="margin-top:18px">${step("Applied","Application submitted",true)}${step("Shortlisted","Recruiter review",o.id===1)}${step("Interview","Awaiting schedule",false)}${step("Outcome","Selected / Rejected",false)}</div></div>`}).join(""):`<div class="empty">No applications yet. Explore recommended opportunities and apply in one flow.</div>`}
 </div>`}

function portfolio(){return `<div class="grid grid-2"><div class="card"><div class="profile-row"><div class="profile-photo">VP</div><div><h2>Varun Pasupula</h2><div class="muted small">CSE • Backend Developer</div></div></div><div class="section-head"><h2>Verified skills</h2><span class="badge-verified">92% profile</span></div><div>${["Python","SQL","Git","Problem Solving","Communication"].map(s=>`<span class="pill green">✓ ${s}</span>`).join("")}</div><div class="section-head"><h2>Projects</h2><button class="link-btn" onclick="toast('Project form opened')">+ Add</button></div>${portfolioItem("Smart Internship Matcher","Python • PostgreSQL • Matching","Verified evidence")}${portfolioItem("REST API Service","FastAPI • SQL • Git","Project evidence")}</div>
 <div class="card"><h3>Portfolio completeness</h3><div style="font:700 42px 'Space Grotesk';margin:12px 0">92%</div><div class="progress"><span style="width:92%"></span></div><div class="feature-list"><div>✓ <span>Identity & institution verified</span></div><div>✓ <span>Skills backed by evidence</span></div><div>✓ <span>Projects added</span></div><div>○ <span>Add internship completion record</span></div></div><button class="btn" style="margin-top:18px" onclick="toast('Shareable portfolio link copied')">Share portfolio</button></div></div>`}
function portfolioItem(t,s,v){return `<div class="opportunity"><div class="op-title">${t}</div><div class="op-company">${s}</div><span class="badge-verified" style="display:inline-block;margin-top:8px">✓ ${v}</span></div>`}

function industryDashboard(){return `<div class="hero"><div class="eyebrow" style="color:#7fe1d2">INDUSTRY INTELLIGENCE</div><h2>Post demand. Discover verified-fit candidates.</h2><p>Define required skills and let the platform rank candidates using eligibility, skill coverage, semantic similarity and explainable fit.</p><button class="btn light" onclick="setPage('post')">Post an opportunity →</button></div>
<div class="grid grid-4" style="margin-top:18px">${statCard("◎","Open opportunities","12","+3 this month")}${statCard("⌁","Candidate matches","186","84 high-fit")}${statCard("◷","Applications","64","18 shortlisted")}${statCard("✓","Avg. time to shortlist","3.2d","−18%")}</div>
<div class="section-head"><h2>Candidate matching preview</h2><button class="link-btn" onclick="setPage('candidates')">View all →</button></div>
<div class="card"><table class="kpi-table"><thead><tr><th>Candidate</th><th>Target</th><th>Skill fit</th><th>Evidence</th><th>Action</th></tr></thead><tbody>${["Varun Pasupula","Ananya Rao","Rahul K"].map((n,i)=>`<tr><td><strong>${n}</strong></td><td>Backend Developer</td><td><span class="match-badge">${84-i*6}%</span></td><td><span class="badge-verified">Verified</span></td><td><button class="link-btn" onclick="toast('Candidate profile opened')">Review</button></td></tr>`).join("")}</tbody></table></div>`}

function postOpportunity(){return `<div class="card"><div class="eyebrow">INDUSTRY → CREATE DEMAND</div><h2 style="margin:4px 0 18px">Post an opportunity</h2><div class="form-grid"><div class="field"><label>Opportunity title</label><input placeholder="e.g. Backend Developer Intern"></div><div class="field"><label>Type</label><select><option>Internship</option><option>Entry-level Job</option><option>Live Project</option><option>Apprenticeship</option></select></div><div class="field"><label>Location</label><input placeholder="Remote / City"></div><div class="field"><label>Duration</label><input placeholder="8 weeks"></div><div class="field full"><label>Description</label><textarea placeholder="Describe the role, outcomes and responsibilities…"></textarea></div><div class="field full"><label>Required skills</label><input placeholder="Python, SQL, REST API, Docker"></div></div><button class="btn" style="margin-top:18px" onclick="toast('Opportunity saved as draft — verification required before publishing')">Create opportunity</button></div>`}
function candidates(){return `<div class="card"><div class="section-head" style="margin-top:0"><h2>Ranked candidate matches</h2><span class="pill green">Backend Developer Intern</span></div>${["Varun Pasupula","Ananya Rao","Rahul K","Meera S"].map((n,i)=>`<div class="match-card"><div><div class="company">${n}</div><div class="muted small">CSE • Backend Developer</div><div class="reason">${i===0?"Python 95%, SQL 88%, backend interest aligned; Docker gap is manageable.":"Strong core-skill coverage with one or two development gaps."}</div></div><div style="text-align:right"><div class="match">${84-i*5}%</div><button class="btn outline" style="margin-top:8px" onclick="toast('Candidate shortlisted')">Shortlist</button></div></div>`).join("")}</div>`}

function institutionDashboard(){return `<div class="grid grid-4">${statCard("◎","Students assessed","1,248","+14%")}${statCard("◈","Avg. readiness","71%","+6%")}${statCard("⌁","Internship participation","63%","+9%")}${statCard("✓","Placement conversion","78%","+11%")}</div>
<div class="section-head"><h2>Cohort skill demand</h2></div><div class="grid grid-2"><div class="card"><h3>Top recurring gaps</h3>${["Cloud fundamentals","Communication","Data structures","API testing","DevOps"].map((s,i)=>skill(s,82-i*10)).join("")}</div><div class="card"><h3>Internship → placement funnel</h3><div class="chart">${[78,64,51,43,34].map((v,i)=>`<div class="bar-wrap"><div class="bar-value">${v}%</div><div class="bar" style="height:${v}%"></div><div class="bar-label">${["Assessed","Applied","Shortlisted","Interview","Selected"][i]}</div></div>`).join("")}</div></div>
<div class="section-head"><h2>Recommended institutional interventions</h2></div><div class="grid grid-3">${learningCard("Cloud Bootcamp","Industry demand","4 weeks","Cloud")}${learningCard("API Testing Lab","Skill gap cohort","2 weeks","API Testing")}${learningCard("Industry Mentor Sprint","Expert-led","6 weeks","Mentorship")}</div>`}

function genericPage(title,desc){return `<div class="card"><div class="eyebrow">${data[state.role].eyebrow}</div><h2>${title}</h2><p class="muted" style="line-height:1.7">${desc}</p><div class="empty">Prototype module ready. Connect this screen to the FastAPI + PostgreSQL backend for production data.</div></div>`}

function renderContent(){
 if(state.role==="student"){
   if(state.page==="dashboard")return studentDashboard();
   if(state.page==="assessment")return assessment();
   if(state.page==="skills")return skillsPage();
   if(state.page==="opportunities")return opportunitiesPage();
   if(state.page==="applications")return applications();
   if(state.page==="learning")return `<div class="grid grid-3">${learningCard("Docker Foundations","Tech Academy","4 weeks","Docker")}${learningCard("API Testing with Postman","Open Learning Lab","2 weeks","API Testing")}${learningCard("Production REST API","SkillBridge Project","3 weeks","REST APIs")}${learningCard("Cloud Fundamentals","Cloud Academy","5 weeks","Cloud")}${learningCard("Communication for Engineers","Career Lab","3 weeks","Soft Skills")}</div>`;
   if(state.page==="portfolio")return portfolio();
 }
 if(state.role==="industry"){
   if(state.page==="dashboard")return industryDashboard();
   if(state.page==="post")return postOpportunity();
   if(state.page==="candidates")return candidates();
   if(state.page==="industryApps")return genericPage("Recruitment applications","Review applicant stages, shortlist candidates and record outcomes.");
   if(state.page==="mentorship")return genericPage("Mentorship programs","Create mentorship cohorts, define goals and track milestones.");
 }
 if(state.role==="institution"){
   if(state.page==="dashboard")return institutionDashboard();
   if(state.page==="students")return genericPage("Student readiness","Inspect cohort-level skill readiness, gaps and evidence-backed portfolios.");
   if(state.page==="analytics")return institutionDashboard();
   if(state.page==="programs")return genericPage("Programs & interventions","Map industry demand to bootcamps, projects and learning programs.");
   if(state.page==="reports")return genericPage("Reports","Export consistent skill, internship and placement metrics for decision-making.");
 }
 if(state.role==="academician"){
   if(state.page==="dashboard")return genericPage("Academician collaboration hub","Discover faculty internships, FDPs, consultancy, research and industrial training.");
   if(state.page==="facultyOps")return genericPage("Faculty opportunities","Browse industrial training and faculty internship opportunities.");
   if(state.page==="fdp")return genericPage("Faculty Development Programs","Find industry-aligned FDPs and workshops.");
   if(state.page==="research")return genericPage("Research partnerships","Connect with organizations for collaborative research projects.");
   if(state.page==="collaboration")return genericPage("Collaboration workspace","Track mentorship, guest lectures, workshops and live projects.");
 }
 return genericPage("Module","This prototype module is ready for backend integration.");
}

function render(){
 document.getElementById("nav").innerHTML=navHTML();
 document.getElementById("roleSelect").value=state.role;
 document.getElementById("portalEyebrow").textContent=data[state.role].eyebrow;
 document.getElementById("pageTitle").textContent=data[state.role].title;
 document.getElementById("content").innerHTML=renderContent();
}
document.getElementById("roleSelect").addEventListener("change",e=>setRole(e.target.value));
document.getElementById("logoutBtn").addEventListener("click",()=>{toast("Demo session ended");});
document.getElementById("notificationBtn").addEventListener("click",()=>toast("3 notifications: shortlist update, new learning match, profile verification"));
document.getElementById("menuBtn").addEventListener("click",()=>document.getElementById("sidebar").classList.toggle("open"));
render();
