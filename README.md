# Agent Skills

Multi-skill repository. It currently provides `containerize` for cross-runtime OCI application and Dev Container engineering with Docker, Podman, Compose, Swarm, Quadlet, and Traefik, plus image-level compatibility for Kubernetes and Cloud Run.

The `containerize` skill designs, reviews, hardens, and validates application images, Dev Containers, and deployments from the application's actual build and runtime contracts. Its routed references cover image construction, development stacks, cache and reproducibility, runtime behavior, supply-chain controls, Docker API security, network isolation, delivery, and evidence-based audits. Kubernetes and Cloud Run platform administration, system containers, Windows containers, HPC containers, and generic software container patterns are outside its scope.

## Install

With the skills CLI:

```bash
npx skills add BorisLord/agent-skills --skill containerize
```

With Agent Skill Manager:

```bash
asm install github:BorisLord/agent-skills --path skills/containerize
```

## Evaluate

The repository pins [skill-up](https://github.com/alibaba/skill-up) through Mise. Install the declared tools, then validate or run the suite locally with an authenticated Codex installation.

```bash
mise install
skill-up validate skills/containerize/evals/eval.yaml
skill-up list-cases skills/containerize/evals/eval.yaml
skill-up run skills/containerize/evals/eval.yaml
```

Reports are written outside the skill directory by default. The six cases cover Compose/Traefik isolation, Swarm compatibility, Docker API authorization boundaries, rootless Podman/Quadlet isolation, Dev Container stack reuse, and the supported-container boundary.

## Layout

```text
skills/
└── containerize/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    └── evals/
        ├── eval.yaml
        └── cases/
```

## License

MIT
