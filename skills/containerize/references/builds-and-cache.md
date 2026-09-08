# Builds, context, and cache

## Layer and cache strategy

Order stable inputs before volatile inputs:

1. base image and system packages;
2. dependency manifests and lockfiles;
3. dependency installation;
4. source code;
5. compilation or asset generation;
6. runtime artifact copy.

Layer ordering alone is insufficient for compiled monorepos. Use engine cache mounts for registries and compiler output where supported. Give concurrent or cross-platform caches distinct IDs when they can corrupt or contaminate each other; use locked sharing when concurrent writers are unsafe.

Scope exported caches by image or build unit so parallel images do not overwrite one default scope. Decide whether feature branches may read a trusted default-branch cache and prevent untrusted builds from writing protected release caches. Set retention from storage quotas, rebuild cost, and last access instead of deleting caches on an arbitrary schedule.

Examples of useful cache targets include npm/pnpm stores, pip/uv caches, Cargo registry plus `target`, Go module/build caches, Maven/Gradle caches, and compiler caches. Do not copy these caches into the final image.

Read [ecosystems-and-cache.md](ecosystems-and-cache.md) for a broader, language-agnostic discovery method and cache validation matrix.

When the compiler output directory is a cache mount, copy the deliverable to a non-mounted path during the same `RUN`; cache-mount contents are not committed into the layer. Cache Cargo Git dependencies separately when the lockfile contains Git sources.

Verify cache behavior by forcing the build step to run after a source-only change. A fully cached Dockerfile layer proves only layer reuse, not the package/compiler cache mount.

## Multi-stage builds

- Name stages and copy only runtime artifacts from builders.
- Do not carry compilers, headers, source trees, package caches, credentials, or test reports into runtime.
- Prefer toolchain-supported production deploy, prune, bundle, publish, or standalone outputs. Avoid deleting arbitrary dependency files by glob: it couples the image to package internals, can break dynamic loading, and may remove required notices.
- Install runtime shared libraries explicitly when the artifact is dynamic.
- Copy certificates or timezone data deliberately for scratch/distroless targets.
- Preserve ownership with `COPY --chown` where supported or set ownership in a controlled layer.

## Build context

The build context is available to the builder even when files are never copied into the final image. Exclude secrets, VCS data, local dependencies, test artifacts, logs, environment files, certificates, keys, and build outputs.

For monorepos:

- keep the workspace root as context when workspace metadata requires it;
- use `<Dockerfile>.dockerignore` for target-specific filtering where supported;
- use named contexts or narrower contexts when they simplify dependency boundaries;
- do not create long fragile `COPY` lists merely to avoid `COPY . .`;
- prefer an allowlist ignore file for tiny security-sensitive contexts such as backup or deployment utilities.

Use `.containerignore` for Podman-specific contexts and `.dockerignore` for portable Docker/Podman contexts. Verify precedence before combining engine-specific and Dockerfile-specific ignore files.

## Multi-platform builds

- Map each OCI platform and variant to an exact compiler target and runtime ABI.
- Do not assume `--platform` cross-compiles binaries or installs CPU emulation.
- Use native runners, a verified cross toolchain, or explicitly provisioned QEMU/binfmt according to the build steps.
- Isolate compiler caches when architectures or incompatible toolchains share the same path.
- Inspect the produced image index and smoke-test every platform; test hardware-specific and legacy CPU targets on real hardware before release.

## Packages and remote inputs

- Combine Debian `apt-get update` and `apt-get install` in one layer and delete package indexes.
- Use `apk add --no-cache`; avoid upgrading every installed package in the Dockerfile. Refresh the pinned base instead.
- Pin package versions or repository snapshots only when the project accepts the maintenance and availability trade-off.
- Verify remote artifacts with a checksum. When using signatures, verify that the signed metadata binds the expected artifact name, version, and platform to its digest; a valid signature for a different or older artifact is not sufficient. Use `ADD --checksum` for simple immutable public inputs; use a controlled downloader for authentication, retries, signatures, or custom extraction.
- Use lockfiles and frozen/locked install modes.
- Pin bootstrap tools and package managers as well as application dependencies. A mutable `latest` installer can invalidate an otherwise locked build.

## Reproducibility

Pin base tags to digests and automate refreshes. Qualify registries explicitly. Remember that package repositories, remote scripts, build timestamps, generated metadata, and network resolution can remain mutable after base pinning.

When byte-for-byte reproducibility matters, also control package snapshots, toolchain versions, source dates, archive ordering, and build provenance. Do not impose this complexity when deterministic dependency selection is sufficient.

## Canonical references

- [Docker cache optimization](https://docs.docker.com/build/cache/optimize/)
- [Docker build contexts and Dockerfile-specific ignore files](https://docs.docker.com/build/concepts/context/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Podman build reference](https://docs.podman.io/en/latest/markdown/podman-build.1.html)
- [Buildah build and remote cache behavior](https://github.com/containers/buildah/blob/main/docs/buildah-build.1.md)
