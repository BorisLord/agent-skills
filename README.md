# Agent Skills

Skills for AI coding assistants.

- [containerize](skills/containerize/SKILL.md): build, review, and secure Docker/Podman images, Dev Containers, and deployments.
- [health-fitness-nutrition-coach](skills/health-fitness-nutrition-coach/SKILL.md): support nutrition, weight goals, training, recovery, and health tracking. Explain medical information without diagnosing or prescribing.
- [blog-writing-skill](skills/blog-writing-skill/SKILL.md): turn ideas into polished, site-aware SEO articles in any language, with author approval and revision.

## Install

With the skills CLI:

```bash
npx skills add BorisLord/agent-skills --skill containerize
npx skills add BorisLord/agent-skills --skill health-fitness-nutrition-coach
npx skills add BorisLord/agent-skills --skill blog-writing-skill
```

With Agent Skill Manager:

```bash
asm install github:BorisLord/agent-skills --path skills/containerize
asm install github:BorisLord/agent-skills --path skills/health-fitness-nutrition-coach
asm install github:BorisLord/agent-skills --path skills/blog-writing-skill
```

## License

MIT
