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

---

# Addendum — 2026-11-13: Linux install, modes and Bob Shell

Added by Claude at Le Tuan's request. All facts below are `VERIFIED` from IBM Bob documentation pages fetched on 2026-11-13. Bob was not installed or run, no account was created, and nothing in the 2026-10-31 section above was changed.

| Topic | Fact and source |
|---|---|
| Bob IDE on Linux | [Installing](https://bob.ibm.com/docs/ide/getting-started/install) lists the operating systems as "macOS, Linux, or Windows". The Linux tab has "Debian" and "Red Hat and Fedora" options. Requirements: "Minimum 4 GB RAM (8 GB recommended)", "At least 500 MB available disk space", an internet connection, and an IBMid to sign in. |
| Modes | [Modes](https://bob.ibm.com/docs/ide/features/modes) lists three built-in modes: Agent, Plan and Ask. Plan mode can edit "Markdown and text files only". Ask mode has no Edit or Execute tool. Browser tools are marked experimental. |
| Subagents and tools | The [IDE welcome page](https://bob.ibm.com/docs/ide) says Bob can spawn subagents and "you approve each spawn before it starts". Bob reads and writes project files, runs terminal commands and uses MCP servers. |
| Bob Shell | The [Bob Shell welcome page](https://bob.ibm.com/docs/shell) describes it as bringing Bob "to your command line", with interactive and non-interactive sessions and the same three kinds of mode. |
| Bob Shell install | [Installing Bob Shell](https://bob.ibm.com/docs/shell/getting-started/install-and-setup) supports macOS, Linux and Windows (and IBM Z). It offers an installation script and an npm package, `@ibm/bob`. The same requirements apply as for the IDE. |
| Bob Shell sign-in | Same page: interactive sessions sign in through IBMid or SSO in the browser. Automation uses an API key with scope "Inference" in the `BOB_API_KEY` environment variable. An API key is a secret: it stays out of the repo. |
| Bob Shell task export | [Slash commands](https://bob.ibm.com/docs/shell/features/slash-commands) lists `/export`: "Export the current task to a file. Usage: /export <json\|markdown> [file-name]". This matters because no full export was found for the IDE (see above). `/status` shows "session status, usage, and version information". |
| Bob Shell built-in commands | The same list has no `/review` command and no rollback command. Custom commands can be added in `.bob/commands/`. |
| Support dates | IDE versions 2.0.2 and 2.1.0 lose support on 2027-01-06. Bob Shell should be 2.0.9 or later. Both dates fall after the contest. |

## Not verified

- Whether Bob Shell and Bob IDE draw on the same Bobcoin balance. They share one login page, but no page read here states it.
- Whether the IDE's rollback and code-review features have an equivalent in Bob Shell beyond the built-in command list.
- The actual trial allowance (50 on the pricing page, 40 on the event page; see Journal §1).

## Recommendation (`RECOMMENDED`, Claude)

Use **Bob IDE** as the main tool for product code:

- The submission must describe "how you used IBM Bob". A screen recording of the IDE (plan, diffs, Bob Findings) is easier for judges to follow than a terminal.
- Rollback, `/review` and the Bobcoin display are documented for the IDE.
- The Nov 15 kickoff has four people looking at one screen.

Bob Shell is worth a short test for one thing: `/export` could give a complete task transcript for `BOB_LOG.md`. Test whether it draws on the same Bobcoin balance before relying on it.
