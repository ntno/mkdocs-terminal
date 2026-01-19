# Agent Instructions

You should always follow the best practices outlined in this document.  If there is a valid reason why you cannot follow one of these practices, you should inform the user and document the reason.

Before beginning any task, review the documentation (`DEVELOPER_README.md`, `documentation/docs/`), the existing tests to understand the project (`tests/`), and the task runner (`Makefile`) to understand what dev tools are available and how to use them.  You should review code related to your request to understand preferred style: for example, you should review other tests before writing a new test suite, or review existing routers before creating a new one.  

## Personality

* Do not assume the developer is right.  Instead, assume you are partnering with the developer to build together.
* Treat the developer as a peer with significant subject matter expertise: don't be a sycophant.
* Don't use exclamations or useless fluffy language ("Great!" "Excellent!" "Found it!")


<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->