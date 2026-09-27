# Destructive container operations

Use this module before proposing or running Docker or Podman commands that remove resources, discard data, or reset engine state. An explanation of what a command does does not itself authorize running it.

## Scope and impact

1. Identify the active Docker context or Podman connection, project, exact resource names or IDs, and whether writable layers, volumes, workspaces, images, caches, or machine state would be lost. Use read-only inspection before cleanup; do not use a broad prune to diagnose an unrelated failure.
2. Prefer a targeted stop or restart when the goal is to recover a service. A requested cleanup of a disposable container can proceed after confirming its writable layer contains no needed data; do not add volume deletion or force flags by default.
3. Before proposing a destructive command as the fix or running it, state the exact scope and expected loss. Get explicit user confirmation for persistent-data deletion, forced removal with unknown state, bulk pruning, or an engine reset. A CLI confirmation prompt is not a substitute for this review, and `--force` must not bypass it.
4. If recovery of persistent data matters, verify the intended backup can be restored before deletion. If the affected resources or losses cannot be established, stop and ask rather than guessing.

Docker examples include `docker compose down -v`, `docker compose rm -v`, volume removal or pruning, `docker rm -f`, `docker system prune`, image or builder pruning, and removal of builders or contexts. Podman examples include volume or pod removal, `podman system prune --volumes`, and `podman system reset`; reset removes pods, containers, images, networks, volumes, machines, and configured storage directories. Check the installed engine's command behavior before applying a rule to another implementation.

## Canonical references

- [Docker destructive-operation guardrails skill](https://github.com/docker/skills/blob/main/skills/docker-destructive-guardrails/SKILL.md)
- [Podman system prune](https://docs.podman.io/en/latest/markdown/podman-system-prune.1.html)
- [Podman system reset](https://docs.podman.io/en/latest/markdown/podman-system-reset.1.html)
