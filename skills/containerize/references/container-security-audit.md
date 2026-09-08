# Container security audit

Use this module for evidence-only reviews and after hardening changes. Start read-only. Ask before mutations unless the user already requested implementation, and keep production outside scope unless it was named explicitly.

## Establish scope

Record the hosts, engines, orchestrators, stacks, environments, ingress path, stateful services, and source-of-truth files. Resolve whether the inspected runtime came from Compose, Swarm, Quadlet, Kubernetes, or another consumer before interpreting fields.

Capture a rollback baseline before behavior-changing work: current configuration, immutable image identities, running replicas/tasks, networks, mounts, published ports, health, and representative application responses. Exclude secret values.

## Inspect effective state

Inspect every in-scope container or service for:

- immutable image identity and update source;
- configured and effective UID/GID;
- privileged mode, host PID/IPC/network, devices, capabilities, `no-new-privileges`, seccomp, AppArmor or SELinux;
- root filesystem mode, writable paths, temporary filesystems, bind mounts, named volumes, and socket mounts;
- published addresses and ports, ingress membership, private networks, aliases, and DNS reachability;
- environment names, secret/config sources, label metadata, and build-context exclusions without printing secret values;
- CPU and memory reservations/limits, PID limits, restart and stop policy;
- image and orchestrator healthchecks, current health, task history, rollout and rollback policy;
- logging driver, delivery destination, rotation and disk growth;
- SBOM, provenance, signature verification, vulnerability results, base age, and refresh process when required by release policy.

Flag the gap between source and effective state. A secure Compose file does not remediate a service still running from an older deployment.

## Test boundaries

Use disposable probes attached only to explicitly named test networks and remove only those probes afterward.

- Prove intended client-to-ingress and proxy-to-application requests.
- Prove application-to-database/cache/queue paths with non-destructive operations.
- Prove representative denied paths between unrelated private stacks and from ingress-only members to private dependencies.
- Verify that internal services cannot be reached through host ports or unintended proxy routes.
- Verify required outbound DNS/TLS and denied egress where an egress policy exists.
- Exercise authentication, dashboard exposure, forwarded-header trust, TLS certificates, security headers, rate limits, and body limits when a reverse proxy owns them.
- If a Docker API proxy exists, prove required discovery/event reads and rejected mutation calls.
- Restart dependencies and the engine or orchestrator component only when authorized; verify recovery, health, routing, logs, and state.
- Send normal termination, observe graceful shutdown, then exercise a failed rollout and rollback in a disposable or explicitly approved environment.

## Report and completion

Prioritize findings by reachable impact and evidence. For each finding give the affected object, observed state, exploit or failure path, smallest durable source-of-truth fix, validation, and rollback consequence. Separate defects, accepted risks, host-hardening dependencies, and controls that the selected engine cannot enforce.

An implementation is complete only when:

- source manifests and effective runtime state agree;
- required flows and application requests pass;
- representative forbidden flows and Docker API mutations fail;
- services recover within measured health and rollout windows;
- logs and storage remain bounded;
- no unrelated stack changed;
- rollback inputs remain available;
- every untested control is stated explicitly.

## Canonical references

- [Docker inspect](https://docs.docker.com/reference/cli/docker/inspect/)
- [Docker service inspect](https://docs.docker.com/reference/cli/docker/service/inspect/)
- [Docker container security](https://docs.docker.com/engine/security/)
- [Docker Compose configuration rendering](https://docs.docker.com/reference/cli/docker/compose/config/)
- [Podman inspect](https://docs.podman.io/en/latest/markdown/podman-inspect.1.html)
