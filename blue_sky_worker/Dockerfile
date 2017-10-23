# DOCKER-VERSION 1.11.1
#
FROM docker.aibs-artifactory.corp.alleninstitute.org/fcollman/render-modules:master

MAINTAINER Tim Fliss <timf@alleninstitute.org>

RUN mkdir -p /at_em_imaging_workflow
COPY execution_runner.py requirements.txt test_requirements.txt /at_em_imaging_workflow/
RUN pip install -r /at_em_imaging_workflow/requirements.txt; \
    pip install -r /at_em_imaging_workflow/test_requirements.txt
