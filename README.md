# Agent Skills

Multi-skill repository. It currently provides `containerize` for cross-runtime OCI application images, Dev Containers, containerized software-artifact builds, and deployments with Docker, Podman, Compose, Swarm, Quadlet, and Traefik, plus image-level compatibility for Kubernetes and Cloud Run.

The `containerize` skill designs, reviews, hardens, and validates application images, Dev Containers, exported software artifacts, and deployments from their actual build, consumer, and runtime contracts. Its routed references cover image and artifact construction, development stacks, cache and reproducibility, runtime behavior, supply-chain controls, Docker API security, network isolation, delivery, and evidence-based audits. Kubernetes and Cloud Run platform administration, system containers, bootable system images, Windows containers, and HPC containers are outside its scope.

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

Reports are written outside the skill directory by default. The eight cases cover Compose/Traefik isolation, Swarm compatibility, Docker API authorization boundaries, rootless Podman/Quadlet isolation, Dev Container stack reuse, the supported-container boundary, signed artifact exports, and the package/system-image boundary.

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
