---
name: containerize
description: Build, review, harden, or debug OCI application images, Dev Containers, and Docker/Podman deployments using Compose, Swarm, Quadlet, or Traefik. Use for image, runtime, supply-chain, and Kubernetes/Cloud Run image-contract work. Excludes platform or Linux host administration and system, Windows, HPC, or non-runtime software containers.
license: MIT
metadata:
  author: BorisLord
  version: "0.1.1"
---

# Containerize

Engineer the smallest container solution that satisfies verified build, runtime, release, and operational contracts. Optimize compatibility, security, reproducibility, operability, and build performance together; image size is only one metric.

Scope is OCI application and development containers. LXC/LXD/Incus/systemd-nspawn, Windows containers, Apptainer/Singularity, and non-runtime software "containers" are unsupported. For Kubernetes and Cloud Run, cover only the image-level container contract, not manifests, clusters, IAM, autoscaling, or platform networking.

## Module routing

Load only the applicable modules; combine them when a task crosses boundaries:

- [design-interview.md](references/design-interview.md) before creating or materially changing behavior;
- [ecosystems-and-cache.md](references/ecosystems-and-cache.md) when discovering toolchain, artifact, dependency, or cache contracts;
- [base-images.md](references/base-images.md) when selecting or changing a builder or runtime base;
- [builds-and-cache.md](references/builds-and-cache.md) for Containerfile construction, monorepos, contexts, and reproducibility;
- [dev-containers.md](references/dev-containers.md) for `devcontainer.json`, development stages, editor integration, and reuse of an existing Compose stack;
- [alternative-builds.md](references/alternative-builds.md) before replacing a Containerfile with Buildpacks, Jib, or another higher-level builder;
- [runtime-and-orchestration.md](references/runtime-and-orchestration.md) for processes, signals, probes, logs, state, and orchestration boundaries;
- [compose-and-swarm.md](references/compose-and-swarm.md) for Compose or Docker Swarm authoring, compatibility, updates, and effective-state validation;
- [traefik-and-network-security.md](references/traefik-and-network-security.md) when Traefik, a shared reverse proxy, multi-stack ingress, or container network isolation is in scope;
- [docker-engine-security.md](references/docker-engine-security.md) when a Docker daemon, API endpoint, socket mount, authorization proxy, rootless mode, or daemon configuration is in scope;
- [podman-and-delivery.md](references/podman-and-delivery.md) for Podman, Buildah, Skopeo, rootless containers, or Quadlet;
- [security.md](references/security.md) for image, secret, privilege, provenance, package, and runtime controls;
- [release-and-deployment.md](references/release-and-deployment.md) for CI publication, immutable promotion, migrations, rollback, and rollout policy;
- [container-security-audit.md](references/container-security-audit.md) for a security audit or after implementing hardening controls.

For a full audit, load `container-security-audit.md` first and then every applicable module.

## Workflow

1. Inspect repository instructions, manifests, lockfiles, build scripts, container configuration, CI, deployment target, installed engine, and current official documentation before asking questions or recommending a pattern.
2. Infer the artifact, ABI, process, state, network, secret, health, shutdown, architecture, and release contracts. For creation or behavior changes, ask one compact confirmation covering only material choices the repository cannot answer; do not block evidence-only audits unnecessarily.
3. Apply every relevant module and preserve existing user changes and choices. Reviews remain evidence-only unless implementation was requested.
4. Validate with the real engine and exact release profiles: render effective configuration, build and inspect the final image, exercise runtime behavior and failure paths, and verify effective deployment state. State every unavailable check; linting is not a successful build.
5. Lead with the outcome or prioritized findings. Give evidence, impact, and the smallest durable fix; distinguish defects, measured improvements, optional trade-offs, and unverified boundaries.
