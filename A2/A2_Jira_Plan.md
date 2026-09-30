# SE Lab 2 — Jira Agile Backlog & Sprint Simulation
**Project:** Automated Rubric Assignment Evaluator (Problem Statement #02, from Lab 1)

Everything below is ready to copy-paste into Jira.

---

## Jira project setup

- Project name: `Automated Rubric Assignment Evaluator`
- Key: `ARAE`
- Template: **Software Development → Scrum → Use template**
- Type: **Company-managed** (the handout requires this; team-managed hides some fields)

---

## Epics (5) — one per functional theme from Lab 1

| Epic | Name | Description (paste into Jira) | Lab 1 reqs |
|---|---|---|---|
| EPIC-1 | Submission Intake & Validation | Let students upload project archives and reject non-conforming ones at the door, before they reach the evaluation queue. | FR-003 |
| EPIC-2 | Automated Evaluation & Rubric Scoring | Queue submissions, run the configured test suite in an isolated sandbox, and produce an itemised rubric breakdown without the evaluator starting it. | FR-001, NFR-001, NFR-002 |
| EPIC-3 | Rubric Configuration & Versioning | Let a Faculty Evaluator author, validate and activate a versioned rubric before the submission window opens. | FR-002 |
| EPIC-4 | Automated Peer Review Distribution | Distribute each evaluated submission to a set number of anonymous peer reviewers, evenly and with no self-assignment. | FR-004 |
| EPIC-5 | Score Override & Audit Trail | Let an evaluator override a criterion score with a written justification, keeping both old and new values in an immutable log. | FR-005 |

---

## User stories (14) — with priority and story points

### EPIC-1 — Submission Intake & Validation

| Story | As a / I want / So that | Priority | Points |
|---|---|---|---|
| 1.1 Upload project archive | **As a** student, **I want** to upload my project as a single archive, **so that** I can submit my work without emailing files to the evaluator. | High | 3 |
| 1.2 Format & size validation | **As a** student, **I want** the system to reject a wrong file type or an oversized archive within 3 seconds, **so that** I find out immediately instead of after the deadline. | High | 5 |
| 1.3 Rule-specific rejection message | **As a** student, **I want** the rejection message to name the exact rule I broke, **so that** I can fix the right thing and resubmit. | Medium | 2 |

### EPIC-2 — Automated Evaluation & Rubric Scoring

| Story | As a / I want / So that | Priority | Points |
|---|---|---|---|
| 2.1 Auto-queue and run test suite | **As a** faculty evaluator, **I want** every valid submission queued and tested automatically, **so that** I don't have to start each evaluation by hand. | High | 8 |
| 2.2 Itemised rubric breakdown | **As a** faculty evaluator, **I want** a per-criterion score breakdown whose line items add up to the total, **so that** I can trust the mark without recomputing it. | High | 5 |
| 2.3 Sandboxed execution | **As a** system administrator, **I want** student code run with no network access and a 60-second CPU limit, **so that** one bad submission can't affect the rest of the queue. | High | 8 |
| 2.4 Handle 100 concurrent submissions | **As a** faculty evaluator, **I want** 100 simultaneous uploads processed with nothing dropped, **so that** the deadline rush doesn't lose anyone's work. | Medium | 5 |

### EPIC-3 — Rubric Configuration & Versioning

| Story | As a / I want / So that | Priority | Points |
|---|---|---|---|
| 3.1 Author a rubric | **As a** faculty evaluator, **I want** to define criteria, max marks and linked test cases, **so that** marking is consistent across the batch. | High | 5 |
| 3.2 Weight validation | **As a** faculty evaluator, **I want** the system to refuse a rubric whose weights don't total 100%, **so that** scores can't come out wrong. | High | 3 |
| 3.3 Rubric versioning | **As a** faculty evaluator, **I want** any edit to a live rubric to create a new version, **so that** two students are never graded against different criteria. | Medium | 5 |

### EPIC-4 — Automated Peer Review Distribution

| Story | As a | Priority | Points |
|---|---|---|---|
| 4.1 Auto-assign peer reviewers | **As a** faculty evaluator, **I want** each submission assigned to k anonymous peer reviewers automatically, **so that** I stop doing the allocation by hand. | Medium | 8 |
| 4.2 No self-assignment rule | **As a** student, **I want** to never be assigned my own submission, **so that** peer review stays fair. | Medium | 3 |

### EPIC-5 — Score Override & Audit Trail

| Story | As a | Priority | Points |
|---|---|---|---|
| 5.1 Override with justification | **As a** faculty evaluator, **I want** to override a criterion score with a written reason, **so that** partly-correct work gets fair credit. | Medium | 5 |
| 5.2 Immutable audit log | **As a** student, **I want** every override to record old score, new score, who and when, **so that** I have something to point at if I appeal. | Low | 3 |

**Totals:** Epic 1 = 10 · Epic 2 = 26 · Epic 3 = 13 · Epic 4 = 11 · Epic 5 = 8 → **68 points**

---

## Sprint plan (two 1-week sprints, as the handout requires)

**Sprint 1 — "Intake and core evaluation" (31 pts)**
Stories 1.1, 1.2, 1.3, 2.1, 2.2, 3.1, 3.2
Sprint goal: a student can submit a valid archive and get an itemised rubric score automatically.
*Simulation:* move all to Done → burndown finishes on/near the guideline.

**Sprint 2 — "Sandbox, peer review and overrides" (37 pts)**
Stories 2.3, 2.4, 3.3, 4.1, 4.2, 5.1, 5.2
Sprint goal: safe execution at scale, plus peer review and appeal-proof overrides.
*Simulation:* leave 5.2 (3 pts) in **In Progress** at completion → carry-over, which gives you a far more interesting burndown to write about.

---

## Reflection answers (adapt in your own words)

1. **Did estimations reflect actual effort?** Mostly. The 8-pointers (2.1, 2.3, 4.1) were correctly flagged as risky — sandboxing and fair allocation both hide algorithmic complexity. 1.3 at 2 points was over-estimated; it was a message-formatting change riding on validation logic already built in 1.2.
2. **Was the backlog well-prioritized?** Yes — the High items (intake, evaluation, rubric authoring) form the minimum path to a usable system. Overrides and the audit log are only meaningful once automatic scores exist, so Low/Medium was right. One correction: 3.2 weight validation should arguably have been done before 2.2, since a bad rubric produces bad breakdowns.
3. **How did the sprint align with the plan?** Sprint 1 tracked close to the guideline. Sprint 2 was committed at 37 points against a 31-point Sprint 1 velocity, and 5.2 carried over — classic sign of planning from optimism rather than from measured velocity.
4. **What did the burndown show about capacity?** A flat opening (work sitting In Progress) then a sharp drop near the end — work wasn't broken down finely enough, so nothing closed early. Realistic team velocity looks like ~31 points per week, so Sprint 3 should be planned at about 31, not 37.

---

## Deliverables checklist

- [ ] Screenshot — Backlog with Epics + User Stories (epic panel open, `E` key)
- [ ] Screenshot — Story points visible on stories
- [ ] Screenshot — Active Sprint board (To Do / In Progress / Done)
- [ ] Screenshot — Burndown chart (Reports → Burndown Chart), both sprints
- [ ] Short document with the 4 reflection answers
- [ ] Keep the Jira workspace live — the instructor checks it in person

---

## Built workspace — actual Jira keys

Site: `https://ojasbinjola.atlassian.net` · Project **ARAE** (company-managed Scrum) · Board 3.

| Key | Type | Item | Priority | Pts | Sprint | Final status |
|---|---|---|---|---|---|---|
| ARAE-1 | Epic | EPIC-1 Submission Intake & Validation | — | — | — | To Do |
| ARAE-2 | Epic | EPIC-2 Automated Evaluation & Rubric Scoring | — | — | — | To Do |
| ARAE-3 | Epic | EPIC-3 Rubric Configuration & Versioning | — | — | — | To Do |
| ARAE-4 | Epic | EPIC-4 Automated Peer Review Distribution | — | — | — | To Do |
| ARAE-5 | Epic | EPIC-5 Score Override & Audit Trail | — | — | — | To Do |
| ARAE-6 | Story | 1.1 Upload project archive | High | 3 | 1 | Done |
| ARAE-7 | Story | 1.2 Format and size validation | High | 5 | 1 | Done |
| ARAE-8 | Story | 1.3 Rule-specific rejection message | Medium | 2 | 1 | Done |
| ARAE-9 | Story | 2.1 Auto-queue and run test suite | High | 8 | 1 | Done |
| ARAE-10 | Story | 2.2 Itemised rubric breakdown | High | 5 | 1 | Done |
| ARAE-13 | Story | 3.1 Author a rubric | High | 5 | 1 | Done |
| ARAE-14 | Story | 3.2 Rubric weight validation | High | 3 | 1 | Done |
| ARAE-11 | Story | 2.3 Sandboxed execution | High | 8 | 2 | Done |
| ARAE-12 | Story | 2.4 Handle 100 concurrent submissions | Medium | 5 | 2 | Done |
| ARAE-15 | Story | 3.3 Rubric versioning | Medium | 5 | 2 | Done |
| ARAE-16 | Story | 4.1 Auto-assign peer reviewers | Medium | 8 | 2 | Done |
| ARAE-17 | Story | 4.2 No self-assignment rule | Medium | 3 | 2 | To Do (carry-over) |
| ARAE-18 | Story | 5.1 Override with justification | Medium | 5 | 2 | Done |
| ARAE-19 | Story | 5.2 Immutable audit log | Low | 3 | 2 | In Progress (carry-over) |

- **ARAE Sprint 1** — 31 pts committed, 31 completed, sprint **closed**.
- **ARAE Sprint 2** — 37 pts committed, 31 completed, 6 pts (ARAE-17, ARAE-19) unfinished. Sprint left **active** so the board can be screenshotted; click **Complete sprint** to close it and push the two items back to the backlog.

Note: Story Points is not on the default company-managed screens, so the field was added to `ARAE: Scrum Default Issue Screen` and `ARAE: Scrum Epic Screen` before estimating. The board's estimation statistic is Story Points.
