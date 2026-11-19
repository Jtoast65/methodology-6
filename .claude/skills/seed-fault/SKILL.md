---
name: seed-fault
description: Demonstrate a pipeline fault, capture failing tests and hook stderr, then restore the exact original code. Use for repeated fault-injection exercises.
allowed-tools: Read, Edit, Write, Bash(python *), Bash(make *), Bash(git diff *), Bash(git status*)
---

# Seed and repair a fault: $ARGUMENTS

1. Read the requested fault and the relevant tests. Save the exact original bytes before editing. Work on one fault at a time.
2. Apply only the requested mutation. Run the specific test that should fail and capture the command, exit code, and complete output. A passing test means the demonstration failed.
3. For a src/ edit, retain the real PostToolUse hook stderr and exit status. If replaying a hook payload outside Claude Code, label it as a replay.
4. Repair the mutation, count actual assistant turns used for the repair, and rerun make test. Restore the raw CSV byte for byte after any raw-data experiment.
5. Append the exact diff, actual red output, hook stderr, repair count, and green output to docs/SEEDED_FAULTS.md. Never invent a run or a turn count.
6. Commit the evidence with a message identifying the fault and its repair. Leave no seeded fault active.

For a Bash copy into data/raw/, the Edit|Write matcher does not run. Demonstrate that blind spot explicitly and run make data to check the immutable-data hash.
