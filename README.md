# SkillBridge — Academia × Industry Collaboration Portal

A frontend-first Smart India Hackathon prototype based on the supplied Academia–Industry Collaboration Portal blueprint.

## Run
Open `index.html` in a browser.

No build step is required. The prototype uses plain HTML, CSS and JavaScript so the demo can run immediately.

## Included demo flows
- Student dashboard
- 5-question skill assessment
- Skill profile and gap analysis
- Explainable opportunity matching
- One-click application + application tracker
- Learning recommendations
- Verified portfolio
- Industry dashboard
- Opportunity posting form
- Ranked candidate matches
- Institution readiness / funnel analytics
- Academician portal placeholders

## Production architecture from the blueprint
Recommended next step:
- Next.js + TypeScript + Tailwind for frontend
- FastAPI + Python for API/business logic
- PostgreSQL + pgvector for system of record and vector search
- Embedding + deterministic ranking service for semantic matching
- Redis/background workers for embeddings and notifications
- Object storage for resumes/certificates/reports
- Server-side RBAC, validation, audit logs and access-controlled file storage

The prototype intentionally keeps business logic lightweight; connect the UI to the backend before treating it as production software.
