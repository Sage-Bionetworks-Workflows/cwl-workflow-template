#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs:
  message: string

outputs:
  echo_out:
    type: string
    outputSource: echo/out

steps:
  echo:
    run: https://raw.githubusercontent.com/Sage-Bionetworks-Workflows/cwl-tool-template/v0.0.16/cwl/echo.cwl
    in:
      message: message
    out: [out]
