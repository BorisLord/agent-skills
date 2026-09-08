# Docker engine security boundary

Use this module when a task includes the Docker daemon, its API or socket, daemon-wide defaults, rootless mode, user namespaces, registry trust, or host-visible ports. Keep general Linux hardening such as SSH, kernel policy, package updates, auditd, and host firewall administration in a host-hardening workflow; report those dependencies without silently changing them.

## Daemon control plane

Treat Docker API access as host-level privilege unless an enforced authorization layer proves otherwise.

- Inventory every Unix socket mount, TCP/SSH endpoint, daemon context, authorization plugin, and member of the Docker group.
- Prefer a local Unix socket with narrow host permissions. For remote administration, use SSH or mutual TLS with authorization; never expose an unauthenticated plaintext daemon endpoint.
- A read-only socket bind is not an API authorization control. Use a deny-by-default authorization or socket proxy and expose only the operations required by the exact client version.
- Put an API proxy on a dedicated private network with only its authorized client. Do not publish its port or join it to shared ingress or application networks.
- Keep credentials and client keys outside images and labels, mount them read-only, and restrict ownership.
- Test a required read and representative denied mutations. A proxy that merely starts or answers `/version` is not proven least privilege.

## Isolation choices

- Prefer application-level numeric non-root users independently of daemon mode.
- Evaluate rootless Docker when its networking, ports, storage, cgroups, and operational limitations fit the host.
- Evaluate user-namespace remapping for rootful Docker before deployment; it changes bind-mount ownership and can conflict with privileged or host-integrated workloads.
- Keep the default seccomp profile or a tested stricter profile. Apply AppArmor or SELinux policy where the host supports it.
- Set daemon-wide `no-new-privileges` only after testing every workload; service-level policy remains visible and portable.
- Grant Docker group membership only to trusted host administrators because it normally permits daemon control.

## Exposure and operations

- Inventory effective published addresses and ports, including IPv4 and IPv6. Prefer loopback or a management address for administrative services.
- Remember that Docker manages host packet-filter rules; validate exposure from another machine rather than assuming a frontend firewall command covers published ports.
- Configure bounded daemon/container logging and prove rotation under the selected log driver. Preserve the stdout/stderr contract for applications.
- Consider `live-restore` when availability during daemon upgrades matters, then test its limits and verify containers reattach correctly after the daemon returns.
- Use explicit address pools when overlapping container and site networks are a real risk.
- Restrict registries and mirrors to trusted endpoints, verify transport and credentials, and keep an image refresh process. Digest pinning without refresh preserves old vulnerabilities.
- Protect daemon configuration and systemd overrides as versioned operational inputs. Validate JSON and daemon startup before restart, retain the previous configuration, and verify every workload after a change.

## Audit evidence

Capture at least:

- engine version, rootless/user-namespace mode, security options, cgroup mode, storage and log drivers;
- daemon listeners and socket ownership;
- Docker group membership and API consumers;
- effective published ports, privileged containers, host namespaces, devices, capabilities, security options, mounts, and writable roots;
- networks and cross-stack reachability;
- restart policies, resource limits, health state, and log rotation;
- the daemon's effective configuration and startup logs after any change.

Sanitize outputs before storing them: inspect metadata can expose environment secrets, labels, registry credentials, mount paths, and internal addresses.

## Canonical references

- [Docker daemon attack surface](https://docs.docker.com/engine/security/#docker-daemon-attack-surface)
- [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/)
- [Docker rootless mode](https://docs.docker.com/engine/security/rootless/)
- [Docker user namespace remapping](https://docs.docker.com/engine/security/userns-remap/)
- [Docker daemon configuration](https://docs.docker.com/reference/cli/dockerd/)
- [Docker live restore](https://docs.docker.com/engine/daemon/live-restore/)
- [Docker packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/)
