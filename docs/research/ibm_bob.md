# IBM Bob documentation check — 2026-10-31

All facts below are `VERIFIED` from IBM Bob pages opened on 2026-10-31. No trial was started and no account was created.

| Topic | Fact and source |
|---|---|
| Trial and pricing | [Pricing](https://bob.ibm.com/pricing) lists a free 30-day trial with 50 Bobcoins and “No payment required.” Monthly plans shown are Pro $20 / 50 Bobcoins, Pro+ $60 / 180, and Ultra $200 / 1,000; IBM says prices may vary by country and taxes. |
| Bobcoins | [Bobcoins documentation](https://bob.ibm.com/docs/ide/account/bobcoins) calls them “resource units that measure your consumption”; each AI action uses a variable amount. Monthly allocations reset each billing cycle. Optional overage is $0.50 per Bobcoin, must be enabled, and resets off monthly. The UI/account administration displays consumption; tokens are not a fixed Bobcoin conversion. |
| Chat and task history | [Chat interface](https://bob.ibm.com/docs/ide/features/chat-interface) shows requests, Bob responses, edits, and commands. Unpinned tasks idle for 30 days are deleted by default; retention can be changed, and history is stored locally without backup or sync. Individual text can be copied. A full task/chat export method was **not found** in the inspected docs. [Reset instructions](https://bob.ibm.com/docs/ide/troubleshooting/ts-reset-application) describe exporting settings, while warning that reset deletes task/chat history. |
| Commit messages | [Commit message guide](https://bob.ibm.com/docs/ide/features/commit-messages) says Bob uses staged or unstaged changes, branch name, and recent commit history to suggest a message. The human reviews/edits it and performs the commit. |
| Code reviews | [Code review guide](https://bob.ibm.com/docs/ide/features/code-reviews) documents `/review`, branch comparisons, optional uncommitted changes, and a Bob Findings panel. Issue validation needs GitHub. |
| Rules | [Custom rules](https://bob.ibm.com/docs/ide/configuration/rules) support global and workspace `.bob/rules/`, mode-specific rule folders, and workspace `AGENTS.md`, which loads by default unless disabled. |
| Latest version shown | The [changelog](https://bob.ibm.com/docs/ide/changelog) lists **2.3.0** first, then 2.2.3; no release date was asserted here. Recent listed features include external file/image attachments and remote-workspace hooks. |

## What we can use as evidence of Bob usage in BOB_LOG.md and the project page

- Keep a dated entry per actual Bob session: task, prompt summary, mode, files changed, and human review outcome. Identify the Bob version and Bobcoin consumption if the UI shows them.
- Link each entry to inspectable repository artifacts: diffs, a human-created commit hash, tests, review findings addressed, and the final project page text. A Bob-suggested commit message alone does not prove implementation work.
- Copy short, relevant Bob responses or findings into the log when useful, since the inspected documentation did not establish full chat export and unpinned local history can expire. Avoid credentials and third-party personal data.
- On the project page, describe the specific work Bob actually performed and cite the corresponding log entry/artifact. Do not claim Bob was used for work performed only by another tool.
