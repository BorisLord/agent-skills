# Alternative image build strategies

Select a build strategy from repository and release constraints, not fashion. Do not replace an understandable Containerfile merely to remove it.

## Containerfile or Dockerfile

Prefer an explicit multi-stage file when the project needs exact OS packages, native compilation, cross-toolchains, several artifacts, unusual runtime files, custom security policy, or predictable behavior across independent builders.

## Cloud Native Buildpacks

Consider Buildpacks when maintained buildpacks support the ecosystem and the team values source detection, standardized lifecycle layers, rebasing, dependency metadata, cache images, and SBOM generation.

Before adoption:

- identify and trust the builder, buildpacks, build image, and run image;
- pin or govern their updates and verify supported architectures;
- confirm required OS packages, native toolchains, build-time secrets, network policy, process types, and runtime user;
- test local and ephemeral-CI caches separately;
- inspect the resulting layers, entrypoint, environment, SBOM, base lineage, and rebase behavior;
- retain an escape path when auto-detection cannot express the runtime contract cleanly.

Buildpacks are multi-language, not universal. Unsupported or highly customized ecosystems remain valid Containerfile workloads.

## Jib

Consider Jib for JVM applications when Maven or Gradle should construct reproducible layered images without a local Docker daemon. Confirm:

- base image and digest/update policy;
- JVM/runtime compatibility and supported target architectures;
- application dependency/resource/class layer boundaries and cache behavior;
- main class, JVM flags, user, ports, creation time, labels, and container arguments;
- registry credentials and whether local-engine or direct-registry output is required.

Jib is an ecosystem-specific option inside a language-agnostic decision process, not the default for non-JVM projects.

## SBOM, provenance, and signatures

- Generate an SBOM from the final image or a build system that accounts for the final runtime contents. Choose SPDX, CycloneDX, or another consumer-supported format.
- Generate provenance that binds source, build inputs, builder identity, and resulting digest when required by policy.
- Sign or attest the immutable image digest after publishing. Avoid treating a mutable tag signature as sufficient identity.
- Verify signatures and attestations against expected identity, issuer, repository, workflow, and transparency-log or offline-bundle policy in CI, deployment admission, or promotion.
- Define retention and discovery for referrers/attestations in every registry and mirror path. Test that copying or promotion preserves required metadata.

## Canonical references

- [Cloud Native Buildpacks](https://buildpacks.io/docs/)
- [Buildpacks cache images](https://buildpacks.io/docs/for-app-developers/how-to/build-inputs/use-cache-image/)
- [Buildpacks SBOM](https://buildpacks.io/docs/features/bill-of-materials/)
- [Jib](https://github.com/GoogleContainerTools/jib)
- [Cosign verification](https://docs.sigstore.dev/cosign/verifying/verify/)
