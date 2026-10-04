# Agent Skills

Skills for AI coding assistants.

- [containerize](skills/containerize/SKILL.md): build, review, and secure Docker/Podman images, Dev Containers, and deployments.
- [health-fitness-nutrition-coach](skills/health-fitness-nutrition-coach/SKILL.md): support nutrition, weight goals, training, recovery, and health tracking. Explain medical information without diagnosing or prescribing.

## Install

With the skills CLI:

```bash
npx skills add BorisLord/agent-skills --skill containerize
npx skills add BorisLord/agent-skills --skill health-fitness-nutrition-coach
```

With Agent Skill Manager:

```bash
asm install github:BorisLord/agent-skills --path skills/containerize
asm install github:BorisLord/agent-skills --path skills/health-fitness-nutrition-coach
```

## License

MIT
