# Docker Compose and Swarm

Use this module whenever authoring, migrating, deploying, or auditing a Compose application or Swarm stack. The Compose Specification, a particular Compose implementation, and `docker stack deploy` are different consumers. Verify the installed versions and never infer support from valid YAML alone.

## Consumer contract

- Identify the exact command used in development, CI, and deployment.
- Validate with the exact consumer without emitting resolved secrets, then inspect the effective configuration and runtime state. For Swarm, treat every `Ignoring unsupported options` warning as an unresolved configuration defect until the effective service state proves the intended control exists another supported way.
- Keep separate deployment files when one shared file would hide meaningful incompatibilities. Duplication of a small manifest is cheaper than ambiguous security behavior.
- Build and push images before `docker stack deploy`; Swarm does not build them. Deploy immutable digests when promotion and rollback identity matter.
- Inspect the resulting containers or Swarm services. A parsed field is not evidence that the runtime enforced it.

## Important semantic differences

- Place Traefik routing labels at service level for Compose and under `deploy.labels` for Swarm.
- Specify the Traefik backend port explicitly for Swarm.
- Treat `depends_on` as startup ordering, not durable readiness. Swarm stacks do not provide the Compose dependency contract; services must tolerate dependency startup and restart through bounded retries and readiness.
- Verify support for `security_opt`, capability controls, read-only roots, temporary filesystems, devices, sysctls, resource limits, restart policies, secrets, configs, healthchecks, and update/rollback settings with the exact consumer.
- Compose implementations may honor parts of `deploy`, while `docker stack deploy` uses its own supported Compose model. Never use one renderer as proof for the other.
- Use Compose secrets only after verifying their implementation and host-file exposure. Swarm secrets are encrypted in transit and at rest in the Raft log and mounted only into assigned tasks, but application handling still matters.
- Use explicit external network names for shared resources. Account for stack prefixing of non-external networks and volumes.

## Swarm availability and updates

- Choose replica count, placement, manager quorum, reservations, limits, restart conditions, update order, parallelism, delay, monitor window, failure ratio, and rollback policy from measured service behavior.
- `start-first` temporarily overlaps old and new tasks. Budget ports, memory, CPU, volumes, migrations, and backward compatibility for that overlap.
- A long deployment is not automatically a fault: `update_config.delay` waits between task groups, while `update_config.monitor` monitors each task update for failure. Account for startup time, `parallelism`, task health, delay, and failure policy when explaining rollout duration; reduce a timing window only when health and rollback evidence support it.
- Health state, traffic eligibility, task restart, update failure, and rollback are separate mechanisms. Test the complete failure path.
- Treat node-local volumes as placement and recovery constraints. A replica count greater than one does not make local state highly available.
- Swarm control-plane traffic is encrypted by default; application data on overlay networks is not. Enable encrypted overlays selectively and measure the performance impact.

## Validation

For Docker Compose, use `docker compose config --quiet` when only validation is needed; the ordinary `config` output can contain interpolated variables and resolved environment files. Capture stdout and stderr separately, preserve the exit status, and sanitize warnings and errors before they reach tool output, logs, or the response because diagnostics may contain interpolated values. When the effective model must be reviewed, select only the needed fields and redact sensitive values before exposure. Quiet validation does not prove that a running container or Swarm service enforces the intended settings.

For every deployment profile:

1. validate with the exact consumer, inspect the relevant effective fields without exposing secrets, and fail on ignored or unsupported security fields;
2. inspect image digest, command, user, mounts, secrets/configs, networks, endpoint ports, privileges, capabilities, read-only state, limits, restart, health, and update/rollback policy;
3. test startup from an empty host or node, dependency delay, dependency restart, normal termination, application failure, and failed rollout;
4. verify allowed network paths and denied cross-stack/backend paths;
5. issue application requests through the real ingress and directly confirm that no unintended host port bypass exists;
6. retain the prior digest and a tested rollback command until the rollout is accepted.

## Canonical references

- [Docker Compose Specification](https://docs.docker.com/reference/compose-file/)
- [Docker Compose config command](https://docs.docker.com/reference/cli/docker/compose/config/)
- [Compose deploy specification](https://docs.docker.com/reference/compose-file/deploy/)
- [Docker stack deployment](https://docs.docker.com/engine/swarm/stack-deploy/)
- [Docker Swarm services](https://docs.docker.com/engine/swarm/services/)
- [Docker Swarm secrets](https://docs.docker.com/engine/swarm/secrets/)
- [Docker overlay networks](https://docs.docker.com/engine/network/drivers/overlay/)
