#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs:
  message: string

outputs:
  echo_out:
    type: string
    outputSource: echo/echo_out

requirements:
  SubworkflowFeatureRequirement: {}

steps:
  echo:
    run: subworkflows/echo-workflow.cwl
    in:
      message: message
    out: [echo_out]
