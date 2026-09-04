# Routing

Read this file for any task that cannot be completed safely as one direct workstream.

## Select the execution mode

Choose the simplest mode that can meet the completion criteria.

| Mode | Use when | Control shape |
| --- | --- | --- |
| Direct | One clear workstream fits the main context | Execute and verify |
| Predictable workflow | Steps and gates are known in advance | Sequential stages with explicit checks |
| Dynamic orchestration | Necessary subtasks depend on discoveries or span several domains | Plan, delegate selectively, integrate, and re-plan from evidence |

Do not escalate to a more complex mode merely because it is available.

## Choose capabilities

For each workstream, use this priority:

1. An applicable installed specialist skill.
2. A purpose-built tool or connector for the requested product or external system.
3. A project-provided script or local tool.
4. A general-purpose tool.
5. A transparent capability-gap report when the required access is unavailable.

Do not copy a specialist skill's domain procedure into Moru. Route the work to it and manage its inputs, authorization, output, and evidence.

## Build the dependency plan

Represent prerequisites before considering parallelism. Common boundaries include investigation before mutation, implementation before publication, and creation before destination verification.

Classify each workstream by its outcome and mutation boundary:

- **Build, change, or fix:** produce the requested artifact and proportionate validation.
- **Review, diagnose, or explain:** remain non-mutating unless a change was also requested.
- **Data investigation:** prefer read-only access and retain the environment, query or filters, and time range needed to support the conclusion.
- **Documentation:** preserve the requested format and destination; an external publication is not complete until the destination is re-checked.
- **Composite work:** connect the above as a dependency graph and keep one owner for the integrated outcome.

## Parallelization gate

Parallelize only when all applicable answers are favorable:

1. Can the workstreams progress without consuming each other's unfinished output?
2. Are their write targets non-overlapping?
3. Can each boundary, evidence requirement, output shape, and stopping condition be stated precisely?
4. Is there one integration owner who can resolve conflicts?
5. Will speed, coverage, or context isolation justify the extra coordination and token cost?

Prefer read-heavy exploration, research, log analysis, test runs, and independent review. Keep tightly coupled or overlapping writes under one owner. If write targets become overlapping during execution, stop concurrent mutation and serialize the remaining work.

Use no more agents than there are genuinely independent workstreams. Follow the current environment's delegation policy; Moru does not create delegation authority by itself.

## Delegated work packet

Every delegated brief must provide:

- `objective`: one outcome owned by this worker;
- `scope`: allowed and excluded targets;
- `inputs`: source artifacts and prerequisite findings;
- `capabilities`: preferred skills or tools when relevant;
- `mutation`: whether changes are allowed and where;
- `evidence`: proof required with the result;
- `output`: the return format needed for integration;
- `stop`: completion, retry, failure, and blocker conditions.

Require the return to distinguish the result, evidence, changes, and unresolved items. Ask for distilled findings and precise locations rather than raw intermediate logs.

## Integration

Wait for every result required by the dependency plan. Merge duplicates, resolve disagreement against evidence, and re-check downstream assumptions after a prerequisite changes. The final answer must be owned by the main integrator rather than copied from worker reports.

