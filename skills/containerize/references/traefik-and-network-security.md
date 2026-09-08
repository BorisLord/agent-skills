# Traefik and container network security

Use this module for Traefik on Docker Engine or Docker Swarm and for any design with a shared container reverse proxy. Verify the installed Traefik and engine versions first: provider names, labels, and supported deployment fields change across releases.

## Trust boundaries

Model four separate paths:

1. public clients to Traefik entrypoints;
2. Traefik to explicitly exposed application frontends;
3. application frontends to their private dependencies;
4. Traefik to the Docker API for service discovery.

The shared ingress network is a reachability boundary, not strong tenant isolation. A compromised member can contact other listening members on that network. Keep its membership minimal and combine it with non-root execution, reduced capabilities, read-only filesystems, application authentication, and host controls.

## Network topology

- Create one stable, explicitly named ingress network for Traefik and routed services. Declare it external in application stacks so redeploying a stack does not replace the shared network.
- Give each stack one or more private networks for application-to-database, cache, queue, and worker traffic. Join only the public-facing application service to ingress.
- Keep databases, caches, queues, workers, migration jobs, socket proxies, and management services off the shared ingress network unless a demonstrated traffic path requires membership.
- Publish only host entrypoints that must accept traffic. A service reached through Traefik normally needs an internal listening port, not a host `ports` mapping. `EXPOSE` and Compose `expose` are metadata, not firewall controls.
- Use a Compose `internal: true` network only when its external isolation matches the workload's required egress. A service that must reach the Internet needs a deliberate egress path; do not weaken every backend network to solve one caller's need.
- In Swarm, use an overlay ingress network shared by Traefik and routed services. Enable overlay encryption when node-to-node application traffic crosses an untrusted network and accept its measured performance cost. `attachable: true` is needed only when standalone containers must join the overlay.
- Use stable explicit network names. Account for Compose and Swarm stack-name prefixing when a network is not external.

For each service, record the allowed inbound peers, outbound destinations, DNS needs, and reason for every network membership. The topology is complete when every required flow succeeds and representative forbidden cross-stack and backend flows fail.

## Provider discovery

- Set `exposedByDefault=false`; require `traefik.enable=true` on every routed container or Swarm service.
- Add provider constraints when multiple trust domains share one daemon or cluster. Use an organization-owned label outside the reserved `traefik.*` namespace and require it in the provider constraint.
- Set a default provider network and override it explicitly when a routed service joins more than one network. Use `traefik.docker.network` with the Docker provider and `traefik.swarm.network` with the Swarm provider supported by the installed Traefik version.
- Define the backend port explicitly when inference is ambiguous. For the Swarm provider, set `traefik.http.services.<name>.loadbalancer.server.port`; current Traefik documentation makes this mandatory for Swarm.
- Put Docker labels at container/service level for the Docker provider. Put Traefik labels under `deploy.labels` for Swarm services; labels on individual tasks are not the Swarm routing contract.
- Keep credentials out of labels. Labels are broadly visible through engine inspection and provider discovery.
- Give router, service, and middleware objects unique, stable names across a shared provider to prevent accidental cross-stack collisions.

## Docker API path

Direct unrestricted access to the Docker API can become host control if Traefik is compromised. A read-only bind of `/var/run/docker.sock` protects the socket file from filesystem writes but does not make Docker API requests read-only.

Prefer, in order supported by the deployment:

1. a least-privilege authorization or socket proxy on a private network used only by Traefik;
2. an authenticated and authorized SSH or mutual-TLS endpoint;
3. a direct socket mount only as an explicitly accepted residual risk.

Build proxy policy from the API calls required by the exact Traefik provider and version. Deny by default, allow required discovery and event reads, deny mutation endpoints, bind the proxy only to its private network, and test both allowed reads and rejected writes. Keep the proxy off public and shared application networks.

## Edge configuration

- Publish HTTPS and the deliberate HTTP-to-HTTPS redirect only. Bind administrative listeners to loopback or a management network.
- Keep `api.insecure=false`. Expose the dashboard through an authenticated router only when operations require it; add an IP allowlist or stronger access control for administrative routes.
- Trust forwarded headers only from known upstream proxy addresses or networks. Avoid insecure forwarded-header trust because clients can forge origin and scheme metadata.
- Use maintained TLS versions and ciphers supported by current Traefik defaults unless a verified compatibility requirement needs an override. Automate certificate renewal and alert before expiry.
- Store ACME state and private keys with restrictive ownership and permissions. Use one writer for ACME state unless the selected Traefik edition and storage backend explicitly support coordination.
- Apply security headers, body limits, rate limits, and authentication according to application behavior. Treat proxy controls as defense in depth, not replacements for authorization and validation in the application.
- Bound access-log volume, exclude sensitive headers, and configure container log rotation. Logs must remain available after task replacement without filling the host filesystem.
- Pin Traefik and extension/plugin artifacts to reviewed immutable identities with an update path. Treat third-party plugins as code executing in the proxy trust boundary.

## Effective-state validation

Validate the source with the exact consumer, then inspect the running objects:

- provider startup logs contain no configuration or permission errors;
- only intended services have Traefik labels and ingress-network membership;
- private dependencies have no published host ports and no ingress membership;
- every router resolves to the intended service, port, entrypoint, TLS policy, and middleware chain;
- HTTP redirects as intended and HTTPS succeeds with the expected certificate and headers;
- dashboard and management endpoints reject unauthenticated public access;
- forged forwarded headers from an untrusted client do not become trusted client identity;
- Traefik can read required discovery data through the Docker API path while representative create, exec, secret, and container mutation requests are denied;
- a disposable container on one private stack network cannot resolve or connect to another stack's private services;
- restart and rolling-update tests preserve routing without exposing old or unintended tasks.

Do not declare the design secure from manifest inspection alone. Record commands, effective state, HTTP results, denied network probes, and rollback steps without capturing secrets.

## Canonical references

- [Traefik Docker provider](https://doc.traefik.io/traefik/reference/install-configuration/providers/docker/)
- [Traefik Swarm provider](https://doc.traefik.io/traefik/reference/install-configuration/providers/swarm/)
- [Traefik Docker routing labels](https://doc.traefik.io/traefik/reference/routing-configuration/other-providers/docker/)
- [Traefik Swarm routing labels](https://doc.traefik.io/traefik/reference/routing-configuration/other-providers/swarm/)
- [Traefik API and dashboard](https://doc.traefik.io/traefik/operations/api/)
- [Docker Compose networks](https://docs.docker.com/reference/compose-file/networks/)
- [Docker bridge networks](https://docs.docker.com/engine/network/drivers/bridge/)
- [Docker overlay network encryption](https://docs.docker.com/engine/network/drivers/overlay/)
