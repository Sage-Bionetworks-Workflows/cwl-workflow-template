# dockstore-tool-template
A template project for setting up a containerized CWL Tool.

# Description

This template sets up an opinionated way to organize Docker, CWL, and
tests for a CWL tool to be published on Dockstore.

## Dockerfile

A Dockerfile should exist in the top level directory of this repository.

## CWL

A directory [cwl](cwl) should contain tool definitions in the CWL language.

## Tests

[`cwltest`](https://github.com/common-workflow-language/cwltest) is used for
testing tools. Add test descriptions to `tests/test-descriptions.yaml`. Each test
added requires a file describing the job inputs that should be added to the
[tests](tests) directory.

## Continuous Deployment and Versioning

This template uses GitHub actions to perform automated versioning, version
bumping, building of tagged Docker images, and pushing images to DockerHub.

### CI
Defined in [.github/workflows/ci.yaml](.github/workflows/ci.yaml), this action
runs on each push to master where the commit does not contain '[skip-ci]'.

### TAG CI
Defined in [.github/workflows/ci.yaml](.github/workflows/tag-ci.yaml), this action
runs on each tag push.

### Credentials

This uses GitHub secrets to store credentials for the GitHub action to push to
the `sagebionetworks` DockerHub account using a service account. All repositories
that are generated from this template will need to have this service account
added to it.

### DockerHub

Ideally, the name of the DockerHub repository should be the same as the GitHub
repository. The workflow uses this name by default as the name of the DockerHub
branch to push to.

### Versioning
Versioning is achieved through git tagging using
[semantic versioning](https://semver.org/). Each push to master will generate an
increment to the patch value, unless the commit contains the string '[skip-ci]'.

Use the release script to do a minor or major release. 
To create a minor release, run `python utils/release.py` from the project root.
To create a major release, run the same command but add the flag `--major`.

The release script has dependencies which can be installed to virtual
environment using [pipenv](https://pipenv.pypa.io/en/latest/). After installing
pipenv, run `pipenv install` to install the dependencies, and `pipenv shell`
to activate the environment.

Alternately, to do a minor or major releases manually:
1. Determine what the tag value will be. For example, to make a minor release from v0.1.22, the next tag would be v0.2.0.
1. In the CWL tools, change the docker version to use that tag, and create a commit like "Update docker version in cwl tools in preparation for minor release"
1. Run the tagging commmand: `git tag v0.2.0`
1. Push the tag: `git push --tags`

Whether you use the release script or create a manual tag, a tag push activates
the `tag-ci.yaml` action instead of the `ci.yaml` action, and builds the docker 
image tagged with the release version number.

#### Branch Versioning
Optionally, you can set up your repository for running the CI action on pushes
to all branches, not just master. This is not the default behavior because it
introduces complexity and requires that you use git in a certain way.

To set this up, in `.github/workflows/ci.yaml`, change `master` to `'*'` in the
event filter ( on > push > branches). This will cause pushes to non-master tags
to also build. They will be tagged with this pattern: <semver>-<git-short-sha>,
e.g. `v1.0.0-197e187`.

If you choose to make this change, for best results we recommend that you also
use the no-fast-forward flag (`--no-ff`) when merging branches to master. Using
that flag will ensure that a new merge commit is created, and CI will run
correctly. Without a new merge commit, versioning won't work correctly.
