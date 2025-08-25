# template-fastapi

This is a template project to be used as a standard, for any Python FastAPI application.

## Repository initialization 

This repository is thought to be used as a template for those hosting services that allow this kind of functionality 
(GitHub and GitLab). In this case, a user can simply select this as a template when creating a new repository in the UI 
of the given hosting service and simply clone locally the newly created repository. 

On the other hand, if the hosting service does not provide this functionality, the user should clone locally this repository, 
keep it updated by pulling its main branch regularly and follow the subsequent steps when creating a new repository:
1. create the new repostory for the current project in the UI of the hosting service, taking care that it is completely empty (no README, .gitignore, etc...)
2. clone the empty repository locally
3. manually copy the content of this template repo except the `.git` folder into the newly cloned empty folder.

When the template had been correctly populated on the local system, the user needs to initialize it by running 
the `bin/init_repo.sh` bash script. 
The script will ask the user: 
    * PROJECT_NAME: the name to be used for the project
    * PROJECT_DESCRIPTION: a short description of the project
    * PROJECT_ID_DEV: the id of the Google Cloud Project that will be used as Development environment
    * PROJECT_ID_PROD: the id of the Google Cloud Project that will be used as Production environment
    * PORT: the port that will be used to expose the serivce in the container
The script will automatically consider the Python version in the current environment (currently only Python versions 
from 3.8 to 3.10 are supported), the remote repository url and will take care of adapting template files according 
to input values, Python version and repository url.

**NOTE:** In the process, you will also be asked if you want to *remove the templates*, 
in order to keep your repository minimal and avoid cluttering. 
Please keep in mind that if you do so, you won't be able to re-initialise the files in your repository again. 

### Repository structure
Once initialized the repository will have this structure
```
PROJECT_DIR
│   README.md
│   Dockerfile      ==>  list of docker instructions to build imge
│   Makefile        ==>  list of make commands
│   LICENESE        ==>  project license
│   pyproject.toml  ==>  project configurations
│   .giattributes   ==>  file that gives attributes to pathnames
│   .gitignore      ==>  list of patterns to ignore with git
│   .dockerignore   ==>  list of patterns to ignore while building docker image
│   .commitlintrc.yaml ==>  configurations for commitlint
│   .pre-commit-config.yaml ==>  configurations for git hooks
│
├───.circleci
│   └──   config.yml  ==> CI and CD workflows with circleci
│
├───.github
│   │   RELEASE-TEMPLATE.md  ==> Template file for release notes, to be updated by realease action
│   │
│   └───workflows
│       │   continous-delivery.yml  ==> CD workflow
│       │   continous-integration.yml  ==> CI workflow
│       └── github-page-build-and-deploy.yml  ==> build and deploy github page with code documentation
│
├───app
│   │   __init__.py  ==> file containing version number
│   │   main.py      ==> application access point
│   │   config.py    ==> configuration classes
│   │   facade.py    ==> facade class
│   │   py.typed     ==> empty file required by mypy to recognize a typed package
│   └───core
│       │   __init__.py
│       ├───adapters  ==> configurations module
│       ├───application
│       │   ├───api ==> utilities module
│       │   │   │   __init__.py 
│       │   │   │   handlers.py ==> module containing base exception handlers.
│       │   │   └── routes.py   ==> module containing the implementation of the Routes, which are classes that collect the endpoints exposed by the application.
│       │   └───signatures ==> utilities module
│       │       │   __init__.py 
│       │       │   requests.py   ==> module containing the pydantic BaseModels representing the requests for the endpoints exposed by the application.
│       │       └── responses.py  ==> module containing the pydantic BaseModels representing the responses provided by the endpoints exposed by the application.
│       └───logic
│           │   __init__.py  
│           │   entities.py    ==> module containing pydantic BaseModels for this application
│           │   exceptions.py  ==> module containing exceptions specific for this application.
│           │   services.py    ==> module containing the services (a.k.a. 'ports') of this application.
│           └── usecases.py    ==> module containing the abstractions, a.k.a. 'usecases', of the services of this application.
│   
├───bin ==> folder that will contain executable files
│
├───config ==> folder to collect app an logging configurations. In this folder shoudl be added further configuration files for dev and prod environments that will overwrite defaults, where required.
│   │   defaults.yaml         ==> defaults app configurations, to be extendend and edited as necessary
│   │   app.dev.yaml          ==> app configurations for development environment, to be extendend and edited as necessary
│   │   app.prod.yaml         ==> app configurations for production environment, to be extendend and edited as necessary
│   │   logConfDefaults.yaml  ==> defaults logging configurations
│   │   logConfDev.yaml       ==> logging configurations for development environment
│   └── logConfProd.yaml      ==> logging configurations for production environment
│   
├───requirements
│   │   requirements.txt      ==> application's closed requirements, as built by make reqs
│   └── requirements_dev.txt  ==> development environment's open requirements, as built by make reqs_dev
│   
├───sphinx ==> sphinx documentation folder containig varius files that will be used to compile code documentations
│   └── ... 
│   
├───tests ==> unit-tests module
│   └── __init__.py
│
└───api_keys ==> folder, ignored by git, to contain secrets
```
