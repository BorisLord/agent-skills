# Podman and daemonless delivery

## Compatibility contract

- Detect Podman version, local versus remote client, rootless versus rootful mode, storage driver, network backend, cgroup version, and SELinux state when relevant.
- When recommending an engine, prefer Podman where rootless daemonless Linux operation or Quadlet integration matches the deployment contract; prefer Docker where Docker Desktop, Buildx, Swarm, or Docker API integrations are required. Keep the Containerfile within the shared OCI-compatible feature set unless a verified engine-specific capability materially helps.
- Use fully qualified image names and explicit registries. Do not depend on interactive short-name resolution.
- Keep Containerfiles within the feature intersection required by every declared builder. Test with each engine; `alias docker=podman` is migration convenience, not compatibility evidence.
- Account for Docker API consumers that require a socket, Compose-provider differences, and engine-specific build/cache flags.

## Rootless runtime

- Inspect subordinate UID/GID mappings and the container image's numeric user before diagnosing volume permissions.
- Choose user-namespace behavior deliberately. `keep-id`, explicit mappings, named volumes, and image-owned directories solve different problems.
- On SELinux hosts, use `:z` for intentionally shared content and `:Z` for private relabeling only after checking the host-path impact. Do not add `:U` blindly; it recursively changes ownership.
- Prefer named volumes for engine-managed state. Validate bind mounts against the real host filesystem, user namespace, and remote-machine boundary.
- Rootless operation reduces host privilege but does not make privileged flags, host namespaces, devices, or broad socket mounts safe.

## Compose, pods, and Quadlet

- Use Compose for a portable multi-container development or host workflow when the selected Podman Compose provider supports the required fields.
- Use a Podman pod only when shared network/lifecycle semantics are intentional; do not use pods to hide independently scalable services.
- Use Quadlet for declarative long-lived Podman containers, pods, networks, volumes, images, or builds managed by systemd on Linux.
- Prefer Quadlet over generated systemd units. Validate generated units and startup ordering with the installed Podman/systemd versions.
- Configure restart, notification, dependencies, timeouts, health, secrets, mounts, auto-update, and user lingering according to the service contract. Do not copy a generic unit unchanged.

## Buildah cache and secrets

Buildah and Podman share container-image tooling but do not copy BuildKit cache flags mechanically:

- enable intermediate layers when the chosen Buildah workflow requires `--layers`;
- configure `--cache-from` and `--cache-to` registries explicitly for ephemeral CI;
- scope remote cache repositories by trust and incompatible platforms;
- use secret mounts, remembering that secret content changes do not themselves invalidate a cached layer;
- verify multi-architecture manifest lists and every referenced platform image.

## Skopeo

Use Skopeo when registry work should not require pulling into a daemon:

- inspect remote manifests and digests;
- copy or mirror between registries and OCI layouts;
- use `--all` when preserving a complete multi-architecture index;
- preserve or verify digests and signatures according to policy;
- keep registry credentials in supported auth files or secret stores, not command history.

## Canonical references

- [Podman manual](https://docs.podman.io/en/latest/markdown/podman.1.html)
- [Podman Quadlet and systemd units](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)
- [Buildah build](https://github.com/containers/buildah/blob/main/docs/buildah-build.1.md)
- [Skopeo](https://github.com/containers/skopeo)
