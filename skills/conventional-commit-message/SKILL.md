---
name: conventional-commit-message
description: Generate accurate repository-wide Conventional Commit messages from git changes. Use this whenever a user asks for a commit message, asks to summarize staged or unstaged repository changes, requests text for `git commit`, or wants a squash/merge commit summary, even if they do not explicitly mention Conventional Commits.
---

# Conventional Commit Message
Generate one high-quality commit message that represents the overall repository change set.

## Why this skill exists
Good commit messages are short, informative, and consistent. Conventional Commits make history easier to scan, automate, and release from.

## Workflow
1. Gather context from version control:
   - Inspect changed files and diff summaries.
   - Prefer staged changes if staged content exists; otherwise use unstaged changes.
   - If both staged and unstaged changes are relevant, mention that and prioritize what the user asked to commit.
2. Identify the dominant intent of the change set:
   - `feat`: new behavior or capability
   - `fix`: bug fix
   - `refactor`: structural change without behavior change
   - `perf`: performance improvement
   - `docs`: documentation only
   - `test`: tests only
   - `build`: build/dependency/package tooling changes
   - `ci`: CI/CD pipeline updates
   - `style`: formatting/style-only edits
   - `chore`: maintenance work not covered above
   - `revert`: reverts a previous change
3. Choose scope carefully:
   - Use a narrow scope when one subsystem clearly dominates (for example `auth`, `api`, `db`, `ui`).
   - Omit scope when changes are broad or cross-cutting.
4. Compose the subject line:
   - Format: `<type>(<scope>): <summary>` or `<type>: <summary>`
   - Use imperative mood, lowercase type/scope, no trailing period.
   - Keep subject concise (target 50-72 chars).
   - Add `!` after type/scope for breaking changes.
5. Compose optional body and footers:
   - Body should explain key changes and reasoning when useful.
   - Add `BREAKING CHANGE: ...` footer for incompatible changes.
   - Include issue references when present (for example `Refs: #123`).

## Decision rules for mixed changes
- If multiple change types exist, pick the type that best captures user-visible impact.
- Do not pick `chore` when a clearer type (like `feat`/`fix`/`refactor`) fits.
- For commit messages representing many unrelated changes, summarize the highest-impact theme in the subject and include other important changes in the body.

## Output format
When the user asks for a commit message, provide:
1. A ready-to-paste commit message block
2. A one-line rationale explaining why that type/scope was chosen

If the user explicitly asks for subject-only output, return only the subject line.

## Quality checks before final answer
- Message accurately reflects actual changed files/diffs.
- Type and scope match the dominant change intent.
- Subject is concise, imperative, and Conventional Commit compliant.
- Breaking changes are signaled with `!` and `BREAKING CHANGE:` footer.
- Avoid vague summaries like "update stuff" or "misc changes".

## Examples
**Example 1**
Input: Added token refresh flow and session expiry checks in auth middleware
Output: `feat(auth): add token refresh and session expiry handling`

**Example 2**
Input: Corrected null-pointer path in order total calculation and added regression test
Output: `fix(orders): prevent null dereference in total calculation`

**Example 3**
Input: Renamed API response fields from snake_case to camelCase across clients
Output:
`feat(api)!: rename response fields to camelCase`
`BREAKING CHANGE: API response field names now use camelCase instead of snake_case.`
