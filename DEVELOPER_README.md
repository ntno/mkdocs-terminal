# Terminal for MkDocs Theme Development
Use this readme to add a feature to this theme or to update the theme documentation.

## Quicklinks

- [Terminal for MkDocs Theme Development](#terminal-for-mkdocs-theme-development)
  - [Quicklinks](#quicklinks)
  - [Developer Setup](#developer-setup)
    - [Prerequisites](#prerequisites)
    - [Fork and Clone Repository](#fork-and-clone-repository)
    - [Confirm Setup](#confirm-setup)
  - [Documentation Updates](#documentation-updates)
    - [Create a Feature Branch](#create-a-feature-branch)
    - [Push Local Branch to Remote Repository](#push-local-branch-to-remote-repository)


## Developer Setup

### Prerequisites
- install [docker](https://docs.docker.com/get-docker/)
- install [Make](https://www.gnu.org/software/make/)

### Fork and Clone Repository
- [Fork mkdocs-terminal](https://github.com/ntno/mkdocs-terminal/fork)  
- Clone your fork: `git clone git@github.com:YOUR_GIT_USERNAME/mkdocs-terminal.git`

### Confirm Setup
Test your system's docker setup by running the documentation site server locally:

```bash
cd mkdocs-terminal  
make serve-docs
```

You should be able to visit [http://0.0.0.0:8080/mkdocs-terminal/](http://0.0.0.0:8080/mkdocs-terminal/) in your browser and view the mkdocs-terminal documentation site.  

If you get a `docker.sock: connect: permission denied` error, you probably need to start the Docker engine on your machine.  
Open the Docker Desktop application and wait until the application indicates that the Docker engine is in a "running" state.  Then retry starting your docker container.  

![engine-starting](documentation/docs/img/developer-setup/engine-starting.png)  
![engine-running](documentation/docs/img/developer-setup/engine-running.png)  

## Documentation Updates

### Create a Feature Branch
Create a local branch to track your updates.  Include the topic of the feature in your branch name.  Example:  

```bash
git checkout -b docs-add-css-override-instructions
```

### Push Local Branch to Remote Repository