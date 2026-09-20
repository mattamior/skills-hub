# Recovery Model

Only a packet-authorized first HARD_RESET has an automatic generation recovery path. Ordinary defaults may permit one; a Subject Pack or route policy can narrow that allowance to zero, never broaden it beyond one.

## One safe fresh retry

Before the first automatic dispatch, require HARD_RESET, resolved dependencies, packet retry eligibility and unused hard_reset_auto_retry_count. Increment/reserve the count before dispatch. Reuse the identical frozen packet and authorized inputs; do not condition on the failed image, redesign the prompt, reassign references or change edit/preview targets.

After the fresh retry produces its result, stop automatic generation regardless of whether it is ACCEPT, HARD_RESET, RETRY_REQUIRED, REFINE_ELIGIBLE or BLOCKED. ACCEPT may proceed to ordinary validated delivery; it is not permission to sample again.

Keep the allowance packet-revision local. Explicit retries do not replenish a used allowance. Import must preserve the consumed budget. Do not fabricate a revision merely to reset it. A genuine Principal-authorized semantic revision is a new packet.

## Other outcomes

RETRY_REQUIRED never retries automatically. Wait for an explicit RETRY or authorized REVISE. Do not treat an operation miss as a hard identity failure to gain automatic sampling.

REFINE_ELIGIBLE requires explicit bounded refinement, named local defects, the exact usable candidate, Canon evidence, and preservation of all passed V1/V2 dimensions. The new attempt receives full validation. Eligibility is not acceptance or continuity admission.

BLOCKED requires dependency repair. Retrieval of a completed result is not a new sample; transport retry must not secretly generate extra images. A changed evidence set or semantic fallback requires revision, not relabeling a retry.

## Pack-specific gates

Calibration or other declared workflows may require Principal review and disable automatic retry. Respect the frozen stricter policy. If legacy consumer instructions disagree about retaining/dropping an auxiliary on reset, record the contradiction and block cutover; never silently modify frozen evidence membership.
