# Experimental Results

This page collects the figures used in the PrepBench paper. The public
repository exposes table-output evaluation and disambiguation metrics for the
`interactive`, `direct`, and `oracle` tracks described in
[EVALUATION.md](EVALUATION.md). Figures about workflow translation are paper
analysis unless a corresponding public workflow evaluator is released.

## Dataset Statistics

PrepBench `v0.1.0` contains 306 cases and 829 input tables in the public release.

![Dataset statistics](assets/dataset_statistics.png)

## Ambiguity

The benchmark categorizes ambiguity by where missing information appears while
translating a natural-language request into an executable preparation program.

![Ambiguity taxonomy](assets/ambiguity_taxonomy.png)

![Ambiguity distribution](assets/ambiguity_distribution.png)

Clarified requests substantially improve table-preparation accuracy across
agents.

![Ambiguity gap across agents](assets/result_ambiguity_gap.png)

## Interaction

Interaction helps agents recover from ambiguous requests, but gains depend on
the model and on question quality.

![Interaction gains across models](assets/result_interaction_gain.png)

![Question budget usage across models](assets/result_question_budget.png)

![Disambiguation recall by ambiguity type](assets/result_disambiguation_recall.png)

## Profiling

Data profiling has uneven effects across agents and irregularity types.

![Profiling gains across models](assets/result_profiling_gain.png)

![Profiling gains by irregularity type](assets/result_profiling_by_irregularity.png)

## Workflow Translation

These figures analyze the paper's workflow-translation setting. They are
included here for completeness, but the current public release centers on
table-output evaluation.

![Translation outcome composition across models](assets/result_workflow_translation.png)

![Translation outcomes by preparation steps](assets/result_workflow_by_steps.png)
