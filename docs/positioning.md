# Product choices and alternatives

File Review helps answer “what should my agent inspect before restructuring?” It supplies a local starting scope and a careful handoff; the agent supplies source understanding and project-specific judgment. It is useful as a small standalone tool and portfolio project. Similar tools exist, and uniqueness or lower token cost has not been demonstrated.

## Existing approaches

| Approach | Where it fits | File Review's choice |
| --- | --- | --- |
| [Aider repository map](https://aider.chat/docs/repomap.html) | Maps important definitions and relationships to help an agent navigate context | Try focused reading before changing cohesive files; no map or parser dependency here |
| [Large File Simplifier](https://github.com/githubnext/agentics/blob/main/docs/large-file-simplifier.md) | GitHub agent workflow producing a refactoring issue and split plan | Local HTML or terminal handoff, no GitHub workflow setup or automatic issue creation |
| [Crispen](https://github.com/Voidious/crispen) | Python refactoring, including splitting oversized Python files | No language-specific transformer and no claim of equivalent analysis |

These primary sources were checked on November 4, 2026. Features may change. They inform the comparison; no third-party implementation, logo or dependency was copied into this edition. There is no bundled integration or inherited claim to their capabilities. Recheck licences before adding any future implementation from another project.

## Deliberate boundaries

Language-independent means measurement and handoff work for readable text in any language. It does not mean File Review understands every language. Adding a parser for one language would create unequal decision quality and extra maintenance without solving cross-language semantics. A future parser would need independent coverage, budgets and evidence; it should not silently change what a recommendation means.

A short request is ready by default; detailed evidence is optional. The starter scope is a size/path heuristic, not a task relevance ranking. Users can select a better scope. Quoted filenames are untrusted data. The agent must read code, callers, state, project rules and tests before proposing concrete destinations, and must stop if it cannot verify them.

The project does not promise token savings. Splitting may increase reading, imports and navigation. A valid future evaluation would compare the same real task and successful result before and after, recording context read, tokens, time and validation. Smaller files alone are not success.

A custom logo is optional. A truthful synthetic demo, readable documentation, reproducible checks and clear product limits are the initial public presentation. No adoption, performance or exclusivity claim belongs in a CV without evidence.
