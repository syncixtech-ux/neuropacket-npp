# Neuropacket / NPP — FAQ

**Is Neuropacket medical?**  
No. It's a standardized *envelope* for human-state signals used for adaptation/UX/analytics. It is not a diagnostic device.

**Why are units and ranges strict?**  
Interoperability. Fixed units/ranges let teams swap devices and software without re-mapping.

**What is `consent_token`?**  
An app-defined token (often a JWT or opaque ID) proving consent context. It travels with the packet.

**What should `retention` look like?**  
ISO-8601 duration (e.g., `P7D` for 7 days, `P30D` for 30 days).

**What does `signature` do in the free version?**  
Free validator checks presence only. Full crypto verification is a paid add-on later.

**Can I add custom fields?**  
Not in the base packet (schema disallows extra fields). Extend by versioning or by adding separate sidecar objects.

**Timestamps?**  
UTC RFC3339 with `Z`, milliseconds optional: `YYYY-MM-DDThh:mm:ss(.sss)Z`.

**State values 0–1—why?**  
Keeps downstream logic simple and model-agnostic (thresholds and blending are portable).

**Where do I start?**  
Validate the examples, copy the template from `docs/index.html`, run the smoke scripts.
