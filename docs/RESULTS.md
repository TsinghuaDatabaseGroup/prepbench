# Paper Results

This page collects figures from the PrepBench paper. They are included as
context for the benchmark design, not as a required reproduction workflow for
leaderboard users.

For leaderboard submissions, use the table-output evaluator described in
[EVALUATION.md](EVALUATION.md) and report the score from `acc.txt`.

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

![Clarification recall by ambiguity type](assets/result_clarification_recall.png)

## Profiling

Data profiling has uneven effects across agents and irregularity types.

![Profiling gains across models](assets/result_profiling_gain.png)

![Profiling gains by irregularity type](assets/result_profiling_by_irregularity.png)

## Workflow Translation

These figures analyze the paper's workflow-translation setting. They are
included here for paper context, but workflow translation is not part of the
public leaderboard interface.

For the restored experimental workflow executor, see
[WORKFLOW_EXECUTION.md](WORKFLOW_EXECUTION.md).

![Translation outcome composition across models](assets/result_workflow_translation.png)

![Translation outcomes by preparation steps](assets/result_workflow_by_steps.png)
