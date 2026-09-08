# Container security

## Build inputs and provenance

- Use trusted official or organization-controlled registries and fully qualified image references.
- Pin images by digest and use an automated updater to surface refreshes as reviewed changes.
- Keep dependency lockfiles and verify downloaded artifacts, release signatures, or checksums.
- Generate SBOM and provenance attestations when the delivery pipeline consumes them.
- Sign published immutable digests when required, and enforce verification against an expected identity and issuer in the promotion or deployment path.
- Do not execute remote installation scripts without pinning and verification.

## Secrets

- Exclude credentials, environment files, private keys, certificates, cloud config, and runtime secret directories from build contexts.
- Use BuildKit/Buildah secret and SSH mounts for build-time authentication.
- Use orchestrator secrets or read-only runtime mounts for runtime credentials.
- Never store secrets in `ARG`, `ENV`, image labels, layers, build logs, Compose files, or Git history.
- Treat build arguments as public metadata: they can appear in image history, generated frontend assets, or provenance attestations. Classify every value by build-time versus runtime and browser-visible versus server-only exposure.
- Treat removal in a later layer as disclosure; earlier layers retain the bytes.

## Image contents

- Keep only runtime packages and artifacts.
- Inspect the final image configuration and deployment override instead of inferring identity solely from the last Dockerfile. An absent or empty effective user normally means container UID 0; an inherited base may already declare a user.
- Prioritize a dedicated non-root numeric UID/GID for network-facing or secret-bearing workloads. Before switching, prepare and test certificate, secret, device, bind-mount, and named-volume permissions; do not solve failures with world-write access.
- Document any demonstrated need for container root, bound it with user namespaces and runtime policy, and remove capabilities unrelated to that need. Rootless Podman or Docker does not make UID 0 inside the container equivalent to an application-level non-root user.
- Avoid setuid tools, shells, and package managers in high-assurance runtime images when they are unnecessary.
- Make ownership and permissions explicit; do not grant world-write access to solve UID problems.
- Rebuild frequently from refreshed bases instead of mutating long-lived containers.

## Runtime controls

Apply controls in deployment configuration and test them:

- read-only root filesystem plus explicit writable mounts;
- dropped Linux capabilities, adding back only those demonstrated necessary;
- `no-new-privileges`;
- default or stricter seccomp/AppArmor/SELinux policies;
- resource limits and bounded temporary storage;
- network policies and explicit ingress/egress;
- no privileged mode, host PID/network, host devices, or broad socket mounts without a documented hardware or operational requirement.

Rootless Docker or Podman reduces daemon/host risk but does not replace in-container non-root execution or runtime policy.

## Vulnerability decisions

A digest pin fixes identity, not freshness. When a fixed package is available:

1. determine why the package exists in the final stage;
2. remove it when it is only a dispensable probe or debugging helper;
3. otherwise refresh the base tag and digest to a build containing the fix;
4. prefer a maintained refreshed base over upgrading the whole distribution inside the Dockerfile;
5. rebuild and scan the final digest for every published architecture.

Do not compare images by raw CVE count alone. Record:

- affected package and whether it is present in the final stage;
- installed and fixed package versions, base digest age, and the automated refresh path;
- severity, exploitability, reachability, and exposure;
- fixed version availability and distro backports;
- scanner distro/version detection accuracy;
- compensating runtime controls and accepted risk owner.

Fail releases on an explicit policy, not an arbitrary count. Avoid switching from glibc to musl solely to make scanner totals smaller.

## Canonical references

- [Docker build secrets](https://docs.docker.com/build/building/secrets/)
- [Docker build input validation](https://docs.docker.com/build/policies/)
- [Podman short-name aliases](https://github.com/containers/image/blob/main/docs/containers-registries.conf.5.md)
- [Kubernetes security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [OCI image specification](https://github.com/opencontainers/image-spec)
- [Cosign signature verification](https://docs.sigstore.dev/cosign/verifying/verify/)
