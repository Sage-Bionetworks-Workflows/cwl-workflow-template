#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs:
  synapseid:
    type: string
  synapse_config:
    type: File

outputs:
  file:
    type: File
    outputSource: synget/filepath

requirements:
  SubworkflowFeatureRequirement: {}

steps:
  synget:
    run: https://raw.githubusercontent.com/Sage-Bionetworks/synapse-client-cwl-tools/v0.1/synapse-get-tool.cwl
    in:
      synapseid: synapseid
      synapse_config: synapse_config
    out: [filepath]
