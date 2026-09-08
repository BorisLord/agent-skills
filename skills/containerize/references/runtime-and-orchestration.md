# Runtime and orchestration

## Process model

Optimize for one service or operational responsibility per container, not one Unix PID. Worker processes created by one server remain one service.

Avoid a process manager when nginx, an application server, a queue worker, a scheduler, or a log agent can be separate containers. Separation gives each service independent:

- failure and restart visibility;
- health and readiness state;
- logs and termination reason;
- CPU/memory requests, limits, and scaling metrics;
- image updates and security boundaries.

Use Compose for related containers on a Docker/Podman host. Use multiple containers or native sidecars in one Pod when components must share lifecycle, network, or volumes. Use separate workloads when they scale or deploy independently.

Multiple services in one container are an exception, not invalid OCI. Require all of the following:

- a clear reason they cannot be separated;
- PID 1 forwards signals and reaps children;
- the container exits when any required child irrecoverably fails;
- restarts are observable rather than hidden forever;
- stdout/stderr identify each service;
- health checks cover every required service;
- resource aggregation and coupled scaling are acceptable.

Use a tiny init (`--init`) only when the main process cannot reap children. Do not add a full init system merely to satisfy a slogan.

## ENTRYPOINT and CMD

- Use exec form so the intended executable receives signals as PID 1.
- Use `ENTRYPOINT` when the image represents a fixed executable.
- Use `CMD` for a replaceable default command or default arguments.
- Allow orchestrators to override command and arguments intentionally.
- Avoid shell form unless shell expansion is required; then end wrapper scripts with `exec` for the long-lived process.

`EXPOSE` documents intended listening ports. It does not publish a port, open a firewall, or enforce security. Add it when the metadata helps users; do not depend on it operationally.

## Health and shutdown

- Test useful behavior rather than PID existence.
- Treat a missing Dockerfile `HEALTHCHECK` as a question, not automatically a defect. Determine whether the image is a long-lived service and whether Compose, Swarm, Kubernetes, Cloud Run, Quadlet, or another supervisor already owns the probe.
- Choose one authoritative probe definition or test every override. Compose and orchestrators can replace an image's `HEALTHCHECK`, so duplicated definitions can drift.
- Test each probe positively and negatively: it must pass when the promised behavior works and fail when that behavior is deliberately unavailable. Validate every runtime role separately so workers, schedulers, migration jobs, and command overrides do not inherit an irrelevant server probe.
- Do not assume an `unhealthy` status restarts a container; health, readiness, restart, update-failure, and traffic-removal semantics depend on the actual platform.
- Account for the probe implementation in the runtime closure. Adding a shell or HTTP client solely for health checking increases packages and attack surface; a native check or orchestrator probe may be cheaper when it provides equivalent evidence.
- For one-shot backup, migration, or batch containers, use exit status, completion deadlines, and last-success monitoring instead of a perpetual healthcheck. For passive listeners or forwarders, choose a native diagnostic that proves required behavior without mutating production data.
- Use startup probes for slow initialization, readiness for traffic eligibility, and liveness only for unrecoverable stuck states.
- Avoid liveness checks that restart healthy-but-busy instances and cause cascading failures.
- Make dependency-aware readiness deliberate; do not turn every transient downstream outage into a restart.
- Handle the platform termination signal, stop accepting new work, drain in-flight work, flush bounded state, and exit before the grace deadline.
- Budget temporary CPU, memory, ports, and state access for old and new tasks that overlap during start-first or surge rollouts.

## Logs and state

- Write logs to stdout/stderr with stable structured fields where useful.
- Do not depend on writable log files inside the image. Use a volume only when an application cannot stream logs.
- Keep databases, uploads, queues, and durable state in explicit volumes or external services.
- A mount hides image content at the same path. For image-populated state or configuration, test both a fresh volume and an existing volume during upgrades; define initialization, migration, ownership, and rollback behavior so persisted files cannot silently mask the new image contents.
- Assume the writable container layer is ephemeral.

## Canonical references

- [Docker: run multiple processes in a container](https://docs.docker.com/engine/containers/multi-service_container/)
- [Kubernetes Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Kubernetes sidecar containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)
- [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)
- [Cloud Run container contract](https://cloud.google.com/run/docs/container-contract)
