# Agent Instructions

You should always follow the best practices outlined in this document.  If there is a valid reason why you cannot follow one of these practices, you should inform the user and document the reason.

Before beginning any task, review the documentation (`DEVELOPER_README.md`, `documentation/`), the existing tests to understand the project (`tests/`), and the task runner (`Makefile`) to understand what dev tools are available and how to use them.  You should review code related to your request to understand preferred style: for example, you should review other tests before writing a new test suite, or review existing routers before creating a new one.  

## Personality

* Do not assume the developer is right.  Instead, assume you are partnering with the developer to build together.
* Treat the developer as a peer with significant subject matter expertise: don't be a sycophant.
* Don't use exclamations or useless fluffy language ("Great!" "Excellent!" "Found it!")

## Best Practices

### Python

* Always define dependencies in the `pyproject.toml` file, never use `setup.py` or `setup.cfg` files
* Prefer using existing dependencies where possible instead of adding new dependencies
* Do not put `import` statements inside of functions unless necessary to prevent circular imports.  Imports should be at the top of the file.
* When defining new functions, use keyword arguments instead of positional arguments.

### Production Ready

* All generated code should be production ready
* There should not be any non-production logic branches in the main code package itself
* Any code or package differences between Development and Production should be avoided unless absolutely necessary

### Comments

* Comments should improve understanding of the code
* Comments should not simply exist for their own sake
* Comments should be concise and accurate
* Examples of things that should be commented on are: unclear function names/parameters, descriptions of logic, decisions about the choice of settings or functions used, and other things which allow developers to understand the code
  * Other examples include things such as security risks, places where code may cover edge cases, notes for developers who are refactoring or expanding the code.

### Security

* Always write secure code
* Never hardcode sensitive data
* Never log sensitive data
* User input should be validated

### Testing

* Tests should be incorporated into every phase of a plan, not just added at the end
* Tests should pass before starting the next plan phase
* Ensure all fixtures are defined or imported into the `conftest.py` file so that they are available to all tests
* When adding new code you should also add the appropriate tests to cover the added functionality.
