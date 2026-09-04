# Contributing

Thanks for helping improve Moru.

## Before changing the skill

- Open an issue before a large change to the operating contract or project-context format.
- Describe an observed failure or a realistic request the change should improve.
- Keep Moru focused on orchestration. Domain-specific procedures belong in specialist skills or separate plugin capabilities.
- Do not add private project documents, credentials, personal paths, or copied internal policies.

## Development

Fork the repository, create a focused branch, and validate the package before opening a pull request.

```powershell
python scripts/validate_plugin.py .
python scripts/package_plugin.py .
```

A useful behavioral check includes:

1. Installation from a local Marketplace followed by a new Codex conversation.
2. A composite implementation request that should complete.
3. A review-only request that must remain non-mutating.
4. A request missing essential authorization that should stop clearly.
5. A project containing `MORU.md`, confirming that registered sources are used without copying their contents into the skill.

## Pull requests

- Keep one behavioral change per pull request when practical.
- Explain the problem, the changed decision rule, and the evidence used to validate it.
- Update `CHANGELOG.md` for user-visible behavior.
- Avoid wording-only churn unless it improves routing, safety, or clarity.
