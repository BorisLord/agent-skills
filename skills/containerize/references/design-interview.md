# Container design interview

Inspect first, then ask only unanswered questions plus one confirmation of inferred behavior. Present inferred answers so the user can correct them. Keep the first round to one compact group; follow up only when an answer exposes another material decision.

## Required decisions for creation or redesign

Ask the applicable questions in plain language:

1. **Purpose**: Is this image for local development, CI, production, release artifacts, or several distinct targets? Must the same image move unchanged between environments?
2. **Execution**: Which engine and version must run and build it: Docker, rootless or rootful Podman, Buildah, a managed builder, or several? Where will it run: direct CLI, Compose, Quadlet/systemd, Kubernetes, Cloud Run, another platform, or offline/air-gapped hosts?
3. **Runtime contract**: What command should start by default, and should callers be able to replace it? Which ports, protocols, health semantics, termination grace period, logs, writable paths, persistent state, devices, and hardware access are required? Which deployment component owns each probe and restart decision?
4. **Build contract**: Which OS/CPU architectures, libc/ABI targets, optional features, and official artifact profiles are supported? Are native builds, cross-compilation, emulation, private dependencies, or network-free builds required? Which exact profiles must CI test, scan, and publish?
5. **Cache behavior**: Should builds favor the fastest warm rebuild, predictable cold builds, minimal remote cache storage, or strict isolation? Is CI ephemeral? May caches be shared across branches, contributors, architectures, or protected releases? Where may remote cache artifacts be stored?
6. **Runtime policy**: Is a shell or interactive debugging required in production? Which UID/GID, rootless mapping, read-only filesystem, capability, secret, volume, and outbound-network constraints apply?
7. **Release policy**: What support window, update cadence, security-fix deadline, and reproducibility level are required? How should base digests and dependencies be refreshed? Must one digest be promoted unchanged, or may public frontend/build configuration produce an image per environment? Are multi-architecture indexes, vulnerability gates, SBOMs, provenance attestations, signatures, admission verification, rollout checks, rollback retention, or coordinated migrations required?
8. **Priorities**: When goals conflict, rank compatibility, build time, startup time, image transfer size, runtime footprint, debuggability, reproducibility, and hardening.

## Adaptive questions

- For a monorepo, ask whether one root context is acceptable and which projects may invalidate or enter each image build.
- For browser or static assets, ask which values are intentionally public and baked into artifacts, which remain server-only at runtime, and whether environment promotion must reuse the same image.
- For multiple services, ask whether they deploy, fail, scale, update, and expose health independently.
- For databases or stateful applications, ask for durability, backup, migration, ownership, and shutdown guarantees.
- For rolling updates, ask whether old and new versions may overlap, whether the cluster has temporary surge capacity, and whether schema/configuration changes are backward-compatible during that overlap.
- For hardware workloads, ask which devices, groups, capabilities, host paths, and target hosts are authorized.
- For an actively developed project without a Dev Container, ask whether to add one and whether its goal is an isolated reproducible toolchain, local production parity, or both. If wanted, ask which local, remote, cloud, and CI consumers must work; whether to reuse the production Containerfile or Compose graph; and which editor, source mount, hot reload, debugger, sibling service, credential, engine access, and host UID requirements apply. Do not leak those requirements into production stages automatically.
- For high-assurance or offline builds, ask which registries, mirrors, package snapshots, signing identities, verification policies, and network phases are permitted.

## Decision rule

Wait for answers when they change the base ABI, build method, published ports, process topology, privileges, persistence, secret handling, cache trust, deployment files, or release verification. Make and disclose a conservative assumption only when the user asks the agent to decide or the choice is safely reversible.
