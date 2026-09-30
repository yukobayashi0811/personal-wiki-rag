---
reviewed: true
origin: curated
topic: Agent Evaluation
description: A controlled experiment for distinguishing model and harness bottlenecks.
---

# Model Swap Experiment

## Procedure

A model swap experiment holds the harness constant, replaces only the model, and observes how much the evaluation score changes.

## Interpretation

If a stronger model does not improve the score, the harness is the likely bottleneck. If scores change sharply with model capability, the model is the more direct bottleneck.

Model swapping differs from ablation: ablation disables a harness component, while a model swap keeps the harness fixed and changes the model.

## Related Notes

- [[wiki/Source Summaries/Evaluating AI Agents|Evaluating AI Agents]] — supplies the complete evaluation framework containing this experiment.

## Sources

- [[raw/Evaluating AI Agents.md#Evaluating Agents|Evaluating AI Agents — Evaluating Agents]]
