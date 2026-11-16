# Software Engineering Lab Portfolio

This repository contains the submissions, implementation work, test cases, reports, and supporting evidence for **Software Engineering Labs 1–7**.

The labs use a common case study, the **Dropshipping Inventory & Order Orchestrator (DIOO)**, for requirements and architecture activities, followed by practical software development, code quality, and testing exercises.

## Lab Overview

| Lab | Topic | Description |
|---|---|---|
| [Lab 1](Lab-1/PES2UG24CS599_LAB1_SE.pdf) | Requirements Engineering & UML Use-Case Modelling | Defines the functional and non-functional requirements for DIOO, including priorities, acceptance criteria, and rationale. Reviews requirement completeness and testability, identifies actors and use cases, and documents the main and alternate use-case flows. |
| [Lab 2](Lab-2/PES2UG24CS599_LAB2_SE.pdf) | Agile Software Development with Jira | Demonstrates Agile project planning in Jira. Creates Epics and User Stories, estimates work using Story Points, prioritizes the product backlog, runs a mock sprint, tracks story progress, and reviews the sprint burndown chart. |
| [Lab 3](Lab-3/PES2UG24CS599_SE_Lab3.pdf) | Component Modelling & Architectural Pattern Selection | Compares layered, client-server, and microservices architectures for DIOO and selects microservices. Models the six main components: API Gateway, Order Manager, Payment Service, Supplier Integration Service, Inventory Sync Service, and Notification Service. Includes the [component diagram](Lab-3/component-diagram.png). |
| [Lab 4](Lab-4/README.md) | Debugging and Repair of a Pygame Application | Works with a Meteor Dodge space-survival game. The exercise focuses on debugging gameplay behaviour and extending the game with laser firing, meteor splitting, shield power-ups, and consecutive-survival score multipliers. Includes the implementation, before/after evidence, and chat history. |
| [Lab 5](Lab-5/tournament_scoreboard.py) | Static Code Analysis | Applies Pylint, Bandit, and Flake8 to a Python tournament scoreboard. Documents security, code-quality, and style findings, the fixes applied, and the results in the [issue log](Lab-5/issues.md) and [reflection](Lab-5/reflection.md). |
| [Lab 6](Lab-6/elevator_dispatch.py) | Statement and Branch Coverage Testing | Tests an elevator-dispatch module covering direction selection, door actions, and elevator selection. Includes separate test suites for statement and branch coverage, along with coverage screenshots. |
| [Lab 7](Lab-7/SE%20LAB%207.pdf) | Property-Based Testing & Robust Input Validation | Uses Hypothesis property-based tests for elevator utility functions that parse floor requests, calculate total travel, and calculate load percentages. Tests valid inputs, malformed inputs, unexpected input types, and edge cases to check correctness and prevent crashes. |

## Repository Structure

```text
SE-LAB/
├── Lab-1/
│   └── PES2UG24CS599_LAB1_SE.pdf
├── Lab-2/
│   └── PES2UG24CS599_LAB2_SE.pdf
├── Lab-3/
│   ├── PES2UG24CS599_SE_Lab3.pdf
│   └── component-diagram.png
├── Lab-4/
│   ├── README.md
│   ├── main.py
│   ├── game/
│   └── Videos/
├── Lab-5/
│   ├── tournament_scoreboard.py
│   ├── issues.md
│   ├── reflection.md
│   └── reports/
├── Lab-6/
│   ├── elevator_dispatch.py
│   ├── test_elevator_dispatch.py
│   ├── CodeCoverageTest_elevator_dispatch.py
│   ├── BranchCoverageTest_elevator_dispatch.py
│   └── coverage screenshots
└── Lab-7/
    ├── SE LAB 7.pdf
    ├── elevator_dispatch.py
    └── test_elevator_dispatch.py
```

## Tools and Technologies

- **Requirements and modelling:** UML use-case and component diagrams
- **Agile planning:** Jira, Epics, User Stories, Story Points, Scrum board, Burndown Chart
- **Application development:** Python and Pygame
- **Static analysis:** Pylint, Bandit, Flake8
- **Testing:** pytest, code coverage, branch coverage, and Hypothesis

