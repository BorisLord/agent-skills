# Agent Skills

- [containerize](skills/containerize/SKILL.md): OCI builds and Docker/Podman deployments.
- [health-fitness-nutrition-coach](skills/health-fitness-nutrition-coach/SKILL.md): health, nutrition and fitness coaching.
- [blog-writing-skill](skills/blog-writing-skill/SKILL.md): site-aware editorial writing.

## Install

For example, install `containerize` with Agent Skill Manager:

```bash
asm install github:BorisLord/agent-skills --path skills/containerize
```

## Development

```bash
mise run setup
mise run check
```

Checks Python and Markdown. Python 3.11+ is supported;
mise selects the development interpreter. Format Markdown with `mise run fmt:markdown`.

## License

MIT
