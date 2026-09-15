# Image and artifact release and deployment

## Build and promotion identity

Prefer this release chain:

1. pass source and dependency quality gates relevant to the deliverable;
2. build once and establish the immutable digest of each image or exported artifact;
3. scan and test those exact bytes, not a tag, filename, or package version that can move concurrently;
4. attach and verify required SBOM, provenance, and signatures;
5. publish, promote, or deploy the same digests when environment-specific build inputs are unnecessary;
6. verify rollout convergence for images or installation and consumer behavior for exported artifacts;
7. retain the prior known-good deliverables and their attestations until rollback policy expires.

Publish human-friendly, commit, release, or environment tags as aliases when useful, but do not use `latest` as the release identity. Pass the built digest between jobs rather than resolving a mutable tag again. If a frontend deliberately embeds environment-specific public values, produce and track distinct immutable digests or redesign runtime configuration; never pretend they are one promotable artifact.

For file and package releases, publish final artifacts together with the checksum manifest, signatures, certificates or verification bundles, SBOMs, and provenance required by the consumer. Verify the published copy with public trust material; successful verification inside the producing build does not prove that publication preserved the bytes or sidecars.

## Configuration phases

Classify configuration before writing `ARG`, `ENV`, Compose, or orchestrator values:

- build-only tool inputs;
- intentionally public values embedded into browser/static artifacts;
- runtime server configuration;
- runtime secrets supplied through the platform's secret mechanism.

A runtime environment variable cannot change a value already compiled or bundled into an artifact. A value named token or key is not secret merely because CI stores it as a secret, and a supposedly public value must still be reviewed for abuse and rotation consequences.

## Pipeline and cache boundaries

- When the user requests CI image or artifact work, first build and exercise the same release profile locally with the real engine when available. Make CI test the candidate image with its configured runtime contract or verify the exported artifact with its native consumer, rather than testing only the editable source checkout. State any target platform or service dependency that cannot be reproduced locally.
- Give independent images or build units separate external cache scopes; otherwise one build may overwrite another's cache.
- Include target platform, toolchain, and other correctness boundaries in cache design, while allowing safe default-branch reuse where the backend already enforces branch visibility.
- Prevent pull requests or other untrusted builds from poisoning caches consumed by protected releases.
- Treat cache export failure according to policy; do not silently turn every protected build into an unexpectedly cold build.
- Align cache, registry, and artifact-retention cleanup with quotas, last access, rebuild cost, rollback windows, multi-architecture outputs, signatures, and attestations.
- Scan before deployment or promotion. If the image must be pushed to scan or attest it, publish to a non-promoted digest first.

## Release profiles

- Enumerate every official combination of Dockerfile target, build arguments, application features, target platform, and runtime base. Do not let an implicit default silently omit a marketed or distributed variant.
- Build and test the exact profile that is published. Aggregate or `all-features` checks are additional evidence, not substitutes when they produce a dependency graph or binary that differs from release artifacts.
- Run vulnerability and dependency policy checks against each distributed profile, including optional native or hardware features that change its dependency closure.
- Make material official-build inputs explicit and fail when they are missing. Record non-secret feature selections and build metadata in provenance so an artifact can be traced to its tested profile.
- Compare CI matrices, release workflows, local task wrappers, and Dockerfile defaults for drift. A feature tested outside the image or package but omitted from its published build remains unverified as a release artifact.

## Rolling updates and migrations

- Confirm whether old and new versions overlap during start-first, surge, blue/green, or canary rollout.
- Reserve temporary capacity for overlapping replicas and account for exclusive host ports, singleton devices, node-local volumes, and leader roles.
- Keep API, configuration, and database changes backward-compatible for the overlap window, or choose a rollout that prevents mixed versions.
- Run schema migrations as a coordinated one-shot release step or prove startup migrations are idempotent and concurrency-safe. Do not let every replica race an unsafe migration.
- Before an authorized destructive state or schema migration, restore the intended backup into a disposable target and verify its schema plus representative application data. A backup artifact that has not passed a restore test is not proven rollback input.
- Define update monitoring, failure thresholds, rollback behavior, termination grace, and post-deploy verification from observed startup and drain times.
- Remember that health status, traffic readiness, restart policy, and rollout failure are different platform signals.

## Canonical references

- [Docker GitHub Actions cache](https://docs.docker.com/build/cache/backends/gha/)
- [Docker SBOM and provenance attestations](https://docs.docker.com/build/ci/github-actions/attestations/)
