# Zed agents — what is configured here, and everything you can configure

Reference for this repository's Zed setup, and a map of what Zed's agent
features let you change. Written against the Zed docs at
<https://zed.dev/docs/ai/> (Zed ≥ v1.4, where Rules were replaced by Skills and
Instructions).

---

## 1. What this repository ships

| Path | What it is | Scope |
| --- | --- | --- |
| `AGENTS.md` | Always-on project instructions, loaded into every Zed Agent thread in this project | this project |
| `.agents/skills/*/SKILL.md` | On-demand skills the agent loads when a task matches, or you invoke with `/name` | this project |
| `.zed/settings.json` | Project editor settings: what the agent can see, formatting, venv, optional MCP servers | this project |
| `.zed/ZED-AGENTS.md` | This file | documentation |

Everything above is committed, so anyone who clones the repository gets the same
agent behaviour. Nothing in it contains a key, a token or a model choice.

Skills currently defined:

- **`new-lesson-notebook`** — scaffold a notebook with the ATRIUM bootstrap
  cell, Colab badge and section structure.
- **`notebook-hygiene`** — check and clean notebooks before committing or
  teaching; ships `scripts/nb_check.py`, which you can also run by hand:
  `python3 .agents/skills/notebook-hygiene/scripts/nb_check.py --fix`
- **`add-dataset`** — add, move or document a dataset in `datasets.yml`.

**Trust:** project-local skills load only from a *trusted* worktree. The first
time you open this project Zed asks; skills and project MCP servers stay off
until you say yes. That is deliberate — a cloned repository cannot inject
instructions into your agent before you have looked at it.

---

## 2. The three agent paths

Zed can run agentic work in three different ways, and they do **not** share
configuration:

| Path | Runs | Uses | Configure in |
| --- | --- | --- | --- |
| **Zed Agent** | Agent Panel | Zed's own tools, skills, instructions, MCP, and a model from your configured LLM providers | Zed settings + this repository |
| **External Agents** (ACP) | Agent Panel | Another agent process — Claude Code, Codex, Copilot, OpenCode, Cursor, Pi… with its own auth and config | `agent_servers` in settings + that agent's own config |
| **Terminal Threads** | Terminal, listed in the threads sidebar | A CLI/TUI (e.g. `claude`) with its native config | `agent.terminal_init_command` + the CLI's own config |

You already run Claude Code as an External Agent (`agent_servers.claude-acp` in
your user settings). Worth knowing: **Zed's skills and instruction loader apply
to the Zed Agent only.** Claude Code reads `CLAUDE.md` and its own
`.claude/skills` natively; Zed reads `AGENTS.md` and `.agents/skills/`. To keep
both harnesses on the same instructions:

```bash
ln -s AGENTS.md CLAUDE.md        # one file, both agents
```

---

## 3. Instructions (always-on context)

Always-on guidance — conventions, tone, constraints. Loaded into every thread.

**Personal**, applies to all your projects:

```
~/.config/zed/AGENTS.md          # %APPDATA%\Zed\AGENTS.md on Windows
```

**Project**: Zed uses the *first* file it finds, in this order, and it overrides
personal instructions where they conflict:

```
.rules → .cursorrules → .windsurfrules → .clinerules →
.github/copilot-instructions.md → AGENT.md → AGENTS.md → CLAUDE.md → GEMINI.md
```

This repository uses `AGENTS.md` (the [agents.md](https://agents.md/) standard).
Note the order: if a `.rules` or `.cursorrules` file ever appears here, it wins
and `AGENTS.md` is ignored.

**Good practice**

- Short. Every thread pays for it in tokens. Aim for one screen and link out.
- Rules the agent cannot work out from the code: conventions, things that broke
  before, what to ask about first. Not a description of the directory tree.
- Say *why*, not just what — "no outputs in notebooks, because a pull on the hub
  turns them into a JSON merge conflict" survives rewording; "clear outputs"
  does not.
- Guidance that only matters for one kind of task belongs in a skill instead.

---

## 4. Skills (on-demand workflows)

A skill is a folder with a `SKILL.md`. The agent sees only the `name` and
`description` of every installed skill in its system prompt, and loads the body
when a task matches — *progressive disclosure*, so a long skill costs nothing
until it is used.

```
Global:         ~/.agents/skills/<name>/SKILL.md      # every project
Project-local:  <project>/.agents/skills/<name>/SKILL.md
```

Same name in both → the project-local one wins. Skills must be **direct
children** of the skills folder; nested folders are not discovered.

```
my-skill/
├── SKILL.md      # required
├── scripts/      # optional — things the agent runs
├── references/   # optional — detail it loads only when needed
└── assets/       # optional — templates, static files
```

`SKILL.md` frontmatter:

| Field | Required | Rules |
| --- | --- | --- |
| `name` | yes | lower case, digits, hyphens; 1–64 chars; no leading/trailing or doubled hyphen; matches the folder name |
| `description` | yes | what it does **and when to use it**; ≤ 1024 characters |
| `disable-model-invocation` | no | `true` hides it from the agent's catalogue — you invoke it by hand only |

**How they get used**

- Automatically, when the description matches the task (the `skill` tool).
- `/skill-name` in the message editor.
- `@skill` and pick from the completion list.

When the agent invokes a skill you wrote, Zed asks for permission (built-in
skills do not prompt). Pre-approve the ones you trust — see §6.

**Good practice**

- Write the description for a matcher, not a human: name the task types and the
  trigger words ("Use when handling PDFs, extracting text, filling forms").
- Body under ~500 lines; push detail into `references/` and link to it.
- Deterministic work belongs in `scripts/`, not in prose the model re-derives
  each time — a script runs the same way every time and costs one tool call.
- Use `disable-model-invocation: true` for anything with consequences: deploys,
  publishing, `git push`, sending mail.
- The whole catalogue (names + descriptions of every installed skill) is capped
  at 50 KB; skills that do not fit are silently dropped. Keep descriptions tight.
- The agent cannot edit `SKILL.md` files without your explicit approval, even in
  a trusted project.

**Managing them**: `agent: manage skills` in the command palette, or
**Settings → AI → Skills** (User tab = global, Project tab = this repository).
`/create-skill` walks you through writing one; `agent: create skill from url`
imports one from a GitHub Markdown URL. The link icon on a skill row copies a
self-contained `zed://skill?data=…` link you can paste to a colleague — nothing
is written to their disk until they review it and press Save.
Community registry: <https://skills.sh> (copy the folder into
`~/.agents/skills/` or `.agents/skills/`; there is no runtime remote loading).

Edits take effect immediately — no restart. Changing a `name` or `description`
invalidates the prompt cache for the running session.

---

## 5. Agent profiles (which tools exist)

`agent.profiles` in your **user** settings. A profile decides which tools are
*available*; permissions (§6) decide whether a call goes through.

Built in: **Write** (everything), **Ask** (read-only), **Minimal** (no project
tools). Custom ones: profile selector → `Configure`, or `agent: manage profiles`.

```json
{
  "agent": {
    "default_profile": "write",
    "profiles": {
      "lessons-review": {
        "name": "Lessons review",
        "enable_all_context_servers": false,
        "context_servers": {},
        "tools": {
          "read_file": true, "grep": true, "find_path": true,
          "list_directory": true, "diagnostics": true, "fetch": true,
          "edit_file": false, "write_file": false, "terminal": false,
          "delete_path": false, "move_path": false, "copy_path": false
        },
        "default_model": { "provider": "zed.dev", "model": "claude-sonnet-4-5" }
      }
    }
  }
}
```

Built-in tools you can switch on and off: `read_file`, `grep`, `find_path`,
`list_directory`, `diagnostics`, `fetch`, `search_web` (Zed Pro), `edit_file`,
`write_file`, `create_directory`, `copy_path`, `move_path`, `delete_path`,
`terminal`, `skill`, `spawn_agent` (subagents with their own context window),
plus LSP-backed ones (`go_to_definition`, `find_references`, `rename_symbol`,
`get_code_actions`, `apply_code_action`) and `create_thread`,
`list_agents_and_models`, `ask_user`.

A read-only profile is the honest way to review someone's notebook without
risking an edit, and the reliable way to force an MCP server's tools to be used:
turn the competing built-ins off.

---

## 6. Tool permissions (whether a call is allowed)

`agent.tool_permissions`, user settings. Regex (Rust syntax, case-insensitive by
default) matched against the tool's input — the command string for `terminal`,
the path for `edit_file`, the URL for `fetch`, the absolute `SKILL.md` path for
`skill`. MCP tools are addressed as `mcp:<server>:<tool>`.

```json
{
  "agent": {
    "tool_permissions": {
      "default": "confirm",
      "tools": {
        "terminal": {
          "default": "confirm",
          "always_allow": [
            { "pattern": "^git\\s+(status|log|diff|branch|show)" },
            { "pattern": "^python3?\\s+-c\\s" },
            { "pattern": "^\\.?/?\\.agents/skills/.*nb_check\\.py" },
            { "pattern": "^(ls|cat|head|tail|rg|grep)\\b" }
          ],
          "always_confirm": [
            { "pattern": "^pip\\s+install" },
            { "pattern": "git\\s+push" },
            { "pattern": "sudo\\s" }
          ],
          "always_deny": [{ "pattern": "^quarto\\s+publish" }]
        },
        "edit_file": {
          "default": "allow",
          "always_deny": [
            { "pattern": "\\.env" },
            { "pattern": "\\.(pem|key)$" }
          ]
        },
        "skill": {
          "default": "confirm",
          "always_allow": [{ "pattern": "/(notebook-hygiene|add-dataset)/SKILL\\.md$" }]
        }
      }
    }
  }
}
```

Precedence, highest first: built-in security rules → `always_deny` →
`always_confirm` → `always_allow` → per-tool `default` → global `default`.
Chained commands (`a && b`) are split and each part checked. The only
unoverridable built-ins are recursive deletes of `/`, `~`, `$HOME`, `.` and `..`.

`"default": "allow"` globally is the "stop asking me" switch. On a machine where
the agent can reach a shared JupyterHub, prefer per-pattern allows.

---

## 7. Sandboxing (what a call can actually reach)

Permissions decide whether a command runs; the sandbox decides what it can touch
once running. Applies to the Zed Agent's `terminal` and `fetch` only — not to
External Agents, Terminal Threads, tasks or your own terminal.

On Linux it needs a non-setuid `bwrap` on `$PATH` (`sudo dnf install bubblewrap`
on Fedora). Default: reads anywhere, writes only inside the project (never
`.git` metadata) plus a fresh `/tmp`, no network until you approve a host.

```json
{
  "agent": {
    "sandbox_permissions": {
      "network_hosts": ["pypi.org", "files.pythonhosted.org",
                        "download.pytorch.org", "huggingface.co",
                        "*.hf.co", "github.com"],
      "write_paths": ["/home/ronald/.cache/huggingface"]
    }
  }
}
```

Other keys: `allow_all_hosts`, `allow_fs_write_all`, `allow_unsandboxed` — all
blunt; grant narrowly instead. Approving "always" in a prompt writes the grant
into this block for you.

---

## 8. MCP servers

`context_servers`, in user settings or in a project's `.zed/settings.json`
(project ones start when the worktree is trusted). Local servers take
`command`/`args`/`env`; remote ones take `url` and optional `headers`, and fall
back to the MCP OAuth flow when no `Authorization` header is set. Install from
**Settings → AI → MCP Servers → Add Server**, or from the extension registry.
Zed supports MCP *tools* and *prompts*, and reloads a server's tool list when it
changes. A green dot on the server row means it is running.

Never commit a token in `.zed/settings.json` — put servers that need secrets in
your user settings.

---

## 9. Models and the rest of `agent.*`

Models are per feature, in user settings:

```json
{
  "agent": {
    "default_model":        { "provider": "zed.dev", "model": "claude-sonnet-4-5" },
    "inline_assistant_model": { "provider": "zed.dev", "model": "claude-sonnet-4-5" },
    "commit_message_model":   { "provider": "zed.dev", "model": "claude-haiku-4-5" },
    "thread_summary_model":   { "provider": "zed.dev", "model": "claude-haiku-4-5" },
    "compaction_model":       { "provider": "zed.dev", "model": "claude-sonnet-4-5" },
    "subagent_model":         { "provider": "zed.dev", "model": "claude-sonnet-4-5" },
    "model_parameters": [{ "provider": "anthropic", "temperature": 0.2 }]
  }
}
```

`model_parameters` entries are matched last to first; omit `provider` or `model`
to apply more broadly. Custom OpenAI-compatible providers go under
`language_models.openai_compatible` (you already have two).

Other keys worth knowing, with their defaults:

| Key | Default | What it does |
| --- | --- | --- |
| `agent.enabled` | `true` | Turns the Agent Panel off. `disable_ai: true` (top level) kills every AI feature |
| `agent.auto_compact` | `{ "enabled": true, "threshold": "90%" }` | Summarises a long thread before it hits the context limit. `threshold` also takes a token count, or a negative number meaning "tokens remaining". `/compact` does it now |
| `agent.commit_message_instructions` | — | Extra rules for generated commit messages |
| `agent.commit_message_include_project_rules` | `true` | Whether `AGENTS.md` is fed into commit-message generation |
| `agent.single_file_review` | `false` | Review agent edits in a normal editor instead of inline cards |
| `agent.expand_edit_card` / `expand_terminal_card` | `true` | Whether diffs and command output start expanded |
| `agent.notify_when_agent_waiting` | `"primary_screen"` | `all_screens`, `never` |
| `agent.play_sound_when_agent_done` | `"never"` | `when_hidden`, `always` |
| `agent.prevent_idle_sleep` | `true` | Keeps the machine awake while a thread runs |
| `agent.terminal_init_command` | `""` | Command auto-run in a new Terminal Thread, e.g. `"claude"` |
| `agent.use_modifier_to_send` | `false` | Require ctrl-enter to send |
| `agent.message_editor_min_lines` | `4` | Height of the composer |
| `agent.thinking_display` | `"auto"` | How reasoning blocks are shown |
| `agent.show_turn_stats` | `false` | Timing per turn |
| `agent.dock` / `sidebar_side` / `default_width` | `left` / `left` / `640` | Panel layout |

Project settings (`.zed/settings.json`) are the right place for editor and
project keys — `file_scan_exclusions`, `private_files`, `languages`,
`context_servers`. **Agent settings are read globally**, so put `agent.*` in
`~/.config/zed/settings.json`; the project's contribution to agent behaviour is
`AGENTS.md` and `.agents/skills/`.

---

## 10. Day-to-day

| Want to | Do |
| --- | --- |
| Open the panel | `agent: new thread`, or the panel icon |
| Load a skill by hand | `/skill-name`, or `@skill` |
| Add project context | `@` in the composer — files, directories, symbols, past threads, skills, diagnostics, branch diffs, images, URLs to fetch |
| Run several agents at once | Threads sidebar — each thread is independent; `spawn_agent` delegates inside one |
| Shrink a long thread | `/compact` |
| Write a commit message | The ✨ button in the Git panel |
| Edit in place, in the editor | `assistant: inline assist` on a selection — also works in the terminal panel |
| Change tools for this thread | Profile selector at the bottom of the composer |
| See what is loaded | The token/context row above the composer |

**Sensible workflow for this repository**

1. Start in the **Ask** profile (or a read-only custom one) when you want the
   agent to explain a notebook or a dataset entry; switch to **Write** when it
   should change something.
2. Let the agent run `nb_check.py`, not the notebook — running a notebook with
   `transformers` downloads model weights and takes minutes.
3. Keep `AGENTS.md` honest. It is the one file that shapes every thread, and a
   stale line in it is worse than no line.
4. Open both this repository and `../atrium-school-ml` in one Zed project when a
   change touches the programme or the setup page; each worktree brings its own
   instructions and skills.
