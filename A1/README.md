# SE Lab 1: Requirements Engineering and UML Use-Case Modelling

**Problem Statement #02, Campus & Academic Operations**
**System:** Automated Rubric Assignment Evaluator

## Deliverables

| # | Deliverable | File |
|---|-------------|------|
| 1 | Requirements table, 5 FRs and 2 NFRs | [`A1_Requirements_Table.pdf`](A1_Requirements_Table.pdf) |
| 2 | UML use-case diagram | [`A1_UseCase_Diagram.pdf`](A1_UseCase_Diagram.pdf) / [PNG](A1_UseCase_Diagram.png) |
| 3 | Use-case flow specification, 1 page | [`A1_UseCase_Flow.pdf`](A1_UseCase_Flow.pdf) |

## Scope

A system that takes in batches of student code submissions, runs the configured test
suite on each one in an isolated environment, and works out a rubric score from the
results. It also hands out peer reviews on its own, which the faculty evaluator
currently has to do by hand.

Primary actors: Student, Faculty Evaluator
Supporting actors: Peer Reviewer, Sandboxed Test Execution Engine, Notification Service

## Requirements summary

| ID | Type | Priority | Summary |
|----|------|----------|---------|
| FR-001 | Functional | High | Queue submissions, run the test suite, produce an itemised rubric breakdown |
| FR-002 | Functional | High | Write and activate a versioned rubric tied to test cases |
| FR-003 | Functional | High | Check archive format, size and structure before queueing |
| FR-004 | Functional | Medium | Hand out peer reviews automatically with no self-assignment |
| FR-005 | Functional | Medium | Override a criterion score with a reason, keeping an audit log |
| NFR-001 | Performance and scalability | High | 100 submissions at once, nothing dropped, memory at or under 1.5 GB |
| NFR-002 | Security | High | Sandboxed execution, no network access, 60 second CPU limit |

## Use-case diagram

![UML use-case diagram](A1_UseCase_Diagram.png)

Relationships modelled:

- `«include»`: UC-01 to UC-02, UC-03 and UC-04; UC-04 to UC-09
- `«extend»`: UC-08 Override Rubric Score extends UC-04, when the evaluator disputes the automatic total
- Generalization: Peer Reviewer is a Student

## Use-case flow

`UC-01 Submit & Auto-Evaluate Project`, written up with preconditions, postconditions,
an eleven step main success scenario and four alternate flows (validation failure,
sandbox policy violation, engine unavailable, and evaluator override).
