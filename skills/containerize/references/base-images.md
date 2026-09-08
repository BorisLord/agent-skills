# Base image selection

Select the builder and runtime independently. A small builder rarely matters; a compatible, cache-efficient builder does.

## Variant trade-offs

| Variant | Prefer when | Avoid when |
|---|---|---|
| Full development image | Builder needs broad toolchains or debugging | Final runtime does not need those tools |
| Debian/Ubuntu slim | Native dependencies target glibc; compatibility and prebuilt artifacts matter | Artifact is static and needs no runtime |
| Alpine | Dependencies support musl, packages come from Alpine, or the target intentionally uses musl | Native wheels/binaries target only glibc or silently compile from source |
| Distroless | Runtime files are known and shell/package manager removal is valuable | Operators require shell debugging or runtime mutation |
| Scratch | Artifact is verified static and all certificates/data/users are supplied explicitly | Any dynamic library, shell, helper, or unknown runtime file is required |

Do not infer libc compatibility from the implementation language. Python, Node, Ruby, Go with CGO, Rust crates with native code, and JVM/.NET native components may depend on C libraries.

## Common ecosystem starting points

These are starting points for investigation, not a supported-language boundary. For any other ecosystem, determine its artifact type, native dependencies, libc/ABI, runtime closure, and maintained official images using the same evidence.

- **Python/Ruby/Node**: Prefer an official slim glibc image when native extensions are unknown. Use Alpine only after the lockfile and a real build prove musl artifacts exist and no expensive source compilation occurs.
- **Go**: For `CGO_ENABLED=0`, consider distroless static or scratch after adding certificates and identity data as required. With CGO, match the builder and runtime ABI and libraries.
- **Rust**: Match the Rust target. Use a musl runtime or static image for `*-unknown-linux-musl`; use a glibc runtime for `*-unknown-linux-gnu`. Inspect the produced binary rather than assuming it is static.
- **JVM**: Use a supported JRE runtime, not a JDK builder image. Prefer official slim, distroless, or vendor-supported runtime variants based on observability requirements.
- **.NET**: Use the matching official runtime or ASP.NET image. Consider chiseled images only when globalization, timezone, and diagnostics requirements are satisfied.
- **Static web assets**: Build with the frontend toolchain, then copy only generated assets into an unprivileged web-server image.
- **Utility containers**: Prefer the distro or official image that provides maintained binary packages. Avoid compiling routine utilities from source merely to retain Alpine.

## Decision evidence

Before changing a base, compare:

1. successful clean build and native dependency availability;
2. build duration with cold and warm caches;
3. compressed transfer and unpacked size;
4. runtime memory/startup if material;
5. supported architectures;
6. vulnerability severity and available fixes;
7. certificates, locale, timezone, identity, and debugging requirements.

Keep the current base when the proposed change has no demonstrated benefit.

## Canonical references

- [Docker build best practices](https://docs.docker.com/build/building/best-practices/)
- [Google distroless images](https://github.com/GoogleContainerTools/distroless)
- [Official Docker images](https://github.com/docker-library/official-images)
