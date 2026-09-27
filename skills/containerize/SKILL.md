---
name: containerize
description: Build, review, harden, or debug OCI application images, Dev Containers, containerized software-artifact builds, and Docker/Podman deployments using Compose, Swarm, Quadlet, or Traefik. Use for image, exported-artifact, runtime, supply-chain, and Kubernetes/Cloud Run image-contract work. Excludes platform or Linux host administration and bootable system, Windows, or HPC images.
license: MIT
metadata:
  author: BorisLord
  version: "0.3.0"
---

# Containerize

Engineer the smallest container solution that satisfies verified build, runtime, release, and operational contracts. Optimize compatibility, security, reproducibility, operability, and build performance together; image size is only one metric.

Scope is OCI application and development containers plus OCI-containerized builds that export software release artifacts such as binaries, APK/DEB/RPM packages, local or tar outputs, checksums, signatures, SBOMs, and provenance. The build container may be an execution environment rather than the deliverable. LXC/LXD/Incus/systemd-nspawn, Windows containers, Apptainer/Singularity, and bootable operating-system, root-filesystem, ISO, disk, or VM images are unsupported. For Kubernetes and Cloud Run, cover only the image-level container contract, not manifests, clusters, IAM, autoscaling, or platform networking.

Classify by the intended output and consumer, not by the presence of a Containerfile. If the output is an `.apkovl.tar.gz`, bootable root filesystem, ISO, disk or VM image, kernel, or initramfs, or the repository uses Alpine `lbu`, `setup-alpine`, `setup-bootable`, or `mkimage` to configure an operating system for boot, identify it as system-image or Linux provisioning work and hand it off to an applicable skill. Do not trigger this handoff for `.apk` packages, `APKBUILD`, `abuild`, or a Containerfile used only to build and export software artifacts.

Docker Sandboxes (`sbx`) and Docker Agent (`docker agent`) are separate AI-agent products. For their configuration or lifecycle, use [docker-ai-products.md](references/docker-ai-products.md) to find the owning official Docker skill. Use this skill only for any image or container-engineering part of a mixed task.

## Module routing

Load only the applicable modules; combine them when a task crosses boundaries:

- [design-interview.md](references/design-interview.md) before creating or materially changing behavior;
- [ecosystems-and-cache.md](references/ecosystems-and-cache.md) when discovering toolchain, artifact, dependency, or cache contracts;
- [base-images.md](references/base-images.md) when selecting or changing a builder or runtime base;
- [builds-and-cache.md](references/builds-and-cache.md) for Containerfile construction, monorepos, contexts, reproducibility, and exported software artifacts;
- [dev-containers.md](references/dev-containers.md) for `devcontainer.json`, development stages, editor integration, and reuse of an existing Compose stack;
- [alternative-builds.md](references/alternative-builds.md) before replacing a Containerfile with Buildpacks, Jib, or another higher-level builder;
- [runtime-and-orchestration.md](references/runtime-and-orchestration.md) for processes, signals, probes, logs, state, and orchestration boundaries;
- [compose-and-swarm.md](references/compose-and-swarm.md) for Compose or Docker Swarm authoring, compatibility, updates, and effective-state validation;
- [traefik-and-network-security.md](references/traefik-and-network-security.md) when Traefik, a shared reverse proxy, multi-stack ingress, or container network isolation is in scope;
- [docker-engine-security.md](references/docker-engine-security.md) when a Docker daemon, API endpoint, socket mount, authorization proxy, rootless mode, or daemon configuration is in scope;
- [podman-and-delivery.md](references/podman-and-delivery.md) for Podman, Buildah, Skopeo, rootless containers, or Quadlet;
- [destructive-operations.md](references/destructive-operations.md) before proposing or running Docker/Podman cleanup, forced removal, pruning, resets, or data-deleting deployment commands;
- [security.md](references/security.md) for image and exported-artifact secrets, signatures, provenance, package, privilege, and runtime controls;
- [release-and-deployment.md](references/release-and-deployment.md) for CI publication and immutable promotion of images or exported software artifacts, migrations, rollback, and rollout policy;
- [container-security-audit.md](references/container-security-audit.md) for a security audit or after implementing hardening controls.

For a full audit, load `container-security-audit.md` first and then every applicable module.

## Workflow

1. Inspect repository instructions, manifests, lockfiles, build scripts, container configuration, CI, deployment target, installed engine, and current official documentation before asking questions or recommending a pattern.
2. Infer the artifact, ABI, process, state, network, secret, signing, health, shutdown, architecture, consumer, and release contracts. For creation or behavior changes, ask one compact confirmation covering only material choices the repository cannot answer; do not block evidence-only audits unnecessarily.
3. Apply every relevant module and preserve existing user changes and choices. Reviews remain evidence-only unless implementation was requested.
4. Validate with the real engine and exact release profiles. For images, render effective configuration, inspect the final image, exercise runtime behavior and failure paths, and verify effective deployment state. For exported artifacts, inspect the export and verify formats, architectures, checksums, signatures, provenance, and consumer behavior. State every unavailable check; linting is not a successful build.
5. Lead with the outcome or prioritized findings. Give evidence, impact, and the smallest durable fix; distinguish defects, measured improvements, optional trade-offs, and unverified boundaries.
