#!/usr/bin/env python3
"""Deterministic Canon contract helpers; no image model, asset fetching, or auto-approval.

Inputs are resolved by an authorized host. JSON manifests and non-secret locators only.
Validators and hook callbacks are explicitly registered by that host, never eval'ed.
"""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import re
from dataclasses import dataclass
from typing import Any, Callable, Mapping

ROUTES = ("SERIES", "EXISTING_SERIES_SHOT", "STANDALONE_SHOT", "PREVIEW_ONLY",
          "CURRENT_SHOT_OPERATION", "CALIBRATION")
ROLES = ("PROTECTED_CANONICAL", "EDIT_TARGET", "PREVIEW_SHOT_REFERENCE",
         "ACCEPTED_CONTINUITY", "EXPLICIT_EXTERNAL_ROLE", "ORIGINAL_PROMPT_REFERENCE")
EXTERNAL = frozenset(("POSE", "CAMERA", "COMPOSITION", "LIGHTING", "WARDROBE",
                      "ENVIRONMENT", "OBJECT", "SECONDARY_SUBJECT", "NON_HUMAN_SUBJECT"))
HARD_REASONS = frozenset(("WRONG_SUBJECT_IDENTITY", "MAJOR_STRUCTURAL_DRIFT",
                          "MAJOR_ANATOMY_OR_GEOMETRY_FAILURE", "EXTERNAL_IDENTITY_CONTAMINATION"))
HOOK_STAGES = ("PRE_GENERATION", "POST_GENERATION", "PRE_VALIDATION",
               "POST_VALIDATION", "PRE_DELIVERY")
PACKET_FIELDS = frozenset(("subject", "route", "operation", "effective_spec", "series_lock",
                           "shot", "canonical_evidence", "external_evidence", "continuity_evidence",
                           "preserve_constraints", "risk_guards", "preprocess_hooks", "postprocess_hooks",
                           "validators", "retry_policy", "delivery_policy", "output_kind"))


class Blocked(ValueError):
    """A required input cannot be resolved without weakening the contract."""
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        super().__init__(f"{code}: {detail}" if detail else code)


def digest(value: Any) -> str:
    """Version-local canonical JSON hash; not a claim of RFC 8785 compatibility."""
    try:
        raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise Blocked("SPEC_UNRESOLVED", "non-JSON or non-finite contract data") from exc
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def new_session(subject: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {"current_subject": copy.deepcopy(subject), "current_route": None, "current_stage": None,
            "series_lock": {}, "target_ratio": None, "identity_gate": {"status": "OPEN"},
            "preview_gate": {"status": "OPEN"}, "shot_registry": {}, "selected_shot": None,
            "current_revision": None, "image_operation_role": None, "edit_target": None,
            "edit_contract": None, "preview_shot_reference": None, "external_reference_mode": "NONE",
            "external_reference_role_map": {}, "accepted_clean_master": None, "continuity_auxiliaries": [],
            "generation_packet": None, "retry_count": 0, "hard_reset_auto_retry_count": 0,
            "validation_report": None, "last_result_classification": None, "last_result_id": None,
            "candidate_clean_master": None, "session_import": None}


def resolve_route(intent: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    if intent.get("calibration"):
        return "CALIBRATION"
    shot = intent.get("shot_id")
    if shot is not None:
        if shot not in state["shot_registry"]:
            raise Blocked("SPEC_UNRESOLVED", "unknown named shot")
        return "EXISTING_SERIES_SHOT"
    if intent.get("current_operation"):
        if state.get("selected_shot") not in state["shot_registry"]:
            raise Blocked("SPEC_UNRESOLVED", "no unique selected shot")
        return "CURRENT_SHOT_OPERATION"
    if intent.get("preview"):
        return "PREVIEW_ONLY"
    return "SERIES" if intent.get("series") else "STANDALONE_SHOT"


def resolve_image_roles(images: list[dict[str, Any]], canonical_ids: set[str],
                        edit_id: str | None = None, preview_ids: set[str] | None = None,
                        continuity_ids: set[str] | None = None,
                        explicit: Mapping[str, list[str]] | None = None) -> list[dict[str, Any]]:
    """Identifier registries MUST come from verified pack/session provenance, not image captions."""
    explicit = explicit or {}
    ids = [i["id"] for i in images]
    if len(ids) != len(set(ids)):
        raise Blocked("SPEC_UNRESOLVED", "duplicate image bindings")
    if edit_id is not None and edit_id not in ids:
        raise Blocked("EDIT_TARGET_UNAVAILABLE")
    if set(explicit) - set(ids):
        raise Blocked("SPEC_UNRESOLVED", "role map references missing image")
    result = []
    for image in images:
        ident = image["id"]
        tests = (ident in canonical_ids, ident == edit_id, ident in (preview_ids or set()),
                 ident in (continuity_ids or set()), ident in explicit, True)
        role = next(r for r, yes in zip(ROLES, tests) if yes)
        result.append({**copy.deepcopy(image), "primary_role": role,
                       "external_roles": list(explicit.get(ident, [])) if role == "EXPLICIT_EXTERNAL_ROLE" else []})
    return result


def route_external(bindings: list[dict[str, Any]], fallback_dimensions: list[str] | None = None) -> list[dict[str, Any]]:
    result = []
    for image in bindings:
        role = image["primary_role"]
        if role not in ("EXPLICIT_EXTERNAL_ROLE", "ORIGINAL_PROMPT_REFERENCE"):
            continue
        allowed = image["external_roles"] if role == "EXPLICIT_EXTERNAL_ROLE" else (fallback_dimensions or [])
        if not allowed or not set(allowed) <= EXTERNAL:
            raise Blocked("SPEC_UNRESOLVED", "external scope missing or attempts identity transfer")
        result.append({"id": image["id"], "authority": "ROLE_SCOPED_EXTERNAL_REFERENCE",
                       "roles": sorted(set(allowed)), "risk_guards": ["NO_EXTERNAL_IDENTITY_TRANSFER"],
                       "source": role})
    return result


def plan_evidence(pack: Mapping[str, Any], shot: Mapping[str, Any]) -> dict[str, Any]:
    """Exact minimum cover for small, already-scoped packs; reject ambiguous/unbounded inputs."""
    groups = {g["id"] for g in pack["canon"]["invariant_groups"]}
    inventory = pack["references"]["inventory"]
    if len({a["id"] for a in inventory}) != len(inventory):
        raise Blocked("SPEC_UNRESOLVED", "duplicate asset id")
    matched = []
    selected_profile = shot.get("reference_profile")
    for profile in pack["references"]["profiles"]:
        match = profile.get("match", {})
        if set(match) - {"views", "framing", "operations"}:
            raise Blocked("SPEC_UNRESOLVED", "unsupported profile matcher")
        if selected_profile is not None and profile["id"] != selected_profile:
            continue
        if all(shot.get(key) in match[plural] for key, plural in (("view", "views"), ("framing", "framing"), ("operation", "operations")) if plural in match):
            matched.append(profile)
    if selected_profile is not None and not matched:
        raise Blocked("SPEC_UNRESOLVED", "selected profile does not match shot")
    required = set(shot.get("required_invariant_groups", []))
    preferred: set[str] = set()
    mandatory: set[str] = set()
    for profile in matched:
        required.update(profile.get("require", {}).get("invariant_groups", []))
        mandatory.update(profile.get("require", {}).get("assets", []))
        preferred.update(profile.get("prefer_assets", []))
    if not required or not required <= groups:
        raise Blocked("SPEC_UNRESOLVED", "missing or unknown invariant coverage")
    cal_assets = set()
    if pack.get("calibration", {}).get("enabled"):
        for profile in pack["calibration"].get("profiles", []):
            if profile.get("generation_eligible") is True and profile.get("diagnostic_only") is False:
                cal_assets.update(profile.get("authority_assets", []))
    candidates = []
    for asset in inventory:
        if asset.get("generation_eligible") is not True or asset.get("diagnostic_only") is not False:
            continue
        if asset.get("authority") == "APPROVED_CALIBRATION" and asset["id"] not in cal_assets:
            continue
        if asset.get("authority") not in ("CANONICAL_VISUAL", "APPROVED_CALIBRATION"):
            continue
        if asset.get("strict_view", False) and shot.get("view") not in asset.get("views", []):
            continue
        if asset["id"] in mandatory or required.intersection(asset.get("visible_regions", [])):
            candidates.append(asset)
    if not mandatory <= {a["id"] for a in candidates}:
        raise Blocked("CANONICAL_EVIDENCE_UNAVAILABLE", "required asset is unavailable/ineligible")
    if len(candidates) > 24:
        raise Blocked("SPEC_UNRESOLVED", "scope inventory to at most 24 relevant assets before exact cover")
    best = None
    for size in range(1, len(candidates) + 1):
        winners = []
        for subset in itertools.combinations(candidates, size):
            coverage = set().union(*(set(a["visible_regions"]) for a in subset))
            if not mandatory <= {a["id"] for a in subset} or not required <= coverage or not any(a["authority"] == "CANONICAL_VISUAL" for a in subset):
                continue
            score = (sum(shot.get("view") not in a.get("views", []) for a in subset),
                     sum(a["id"] not in preferred for a in subset),
                     sum(a["authority"] != "CANONICAL_VISUAL" for a in subset),
                     len(coverage - required), tuple(sorted(a["id"] for a in subset)))
            winners.append((score, subset))
        if winners:
            best = min(winners, key=lambda pair: pair[0])[1]
            break
    if best is None:
        raise Blocked("CANONICAL_EVIDENCE_UNAVAILABLE", ", ".join(sorted(required)))
    return {"required_invariant_groups": sorted(required), "matched_profiles": sorted(p["id"] for p in matched),
            "canonical_evidence": copy.deepcopy(sorted(best, key=lambda a: a["id"])),
            "coverage": {g: sorted(a["id"] for a in best if g in a["visible_regions"]) for g in sorted(required)}}


@dataclass(frozen=True)
class FrozenPacket:
    serialized: str
    semantic_hash: str

    @property
    def data(self) -> dict[str, Any]:
        return json.loads(self.serialized)


def freeze_packet(packet: Mapping[str, Any]) -> FrozenPacket:
    p = copy.deepcopy(dict(packet))
    missing = PACKET_FIELDS - p.keys()
    if missing or p.get("route") not in ROUTES or not p.get("effective_spec"):
        raise Blocked("SPEC_UNRESOLVED", f"packet shape or route invalid; missing={sorted(missing)}")
    if not p["subject"].get("id") or not p["subject"].get("pack_revision"):
        raise Blocked("SUBJECT_PACK_UNAVAILABLE")
    if not p["canonical_evidence"]:
        raise Blocked("CANONICAL_EVIDENCE_UNAVAILABLE")
    if p["operation"] == "EDIT" and (not p.get("edit_target") or not p.get("edit_contract")):
        raise Blocked("EDIT_TARGET_UNAVAILABLE")
    scope_hash = digest({key: p[key] for key in ("subject", "effective_spec", "series_lock", "shot", "output_kind")})
    for gate in p.get("gates", []):
        if gate.get("required") and (gate.get("status") != "PASSED" or not gate.get("evidence_id") or gate.get("scope_hash") != scope_hash):
            raise Blocked("GATE_NOT_SATISFIED")
    if p["output_kind"] not in ("FINAL", "IDENTITY_CHECK", "PREVIEW", "DIAGNOSTIC", "CALIBRATION"):
        raise Blocked("SPEC_UNRESOLVED", "unknown output kind")
    if p["retry_policy"].get("automatic_hard_reset", 0) not in (0, 1):
        raise Blocked("SPEC_UNRESOLVED", "automatic retry cap exceeds one")
    for item in p["external_evidence"]:
        if item.get("authority") != "ROLE_SCOPED_EXTERNAL_REFERENCE" or not item.get("roles") or not set(item["roles"]) <= EXTERNAL:
            raise Blocked("SPEC_UNRESOLVED", "invalid external evidence authority/roles")
    for item in p["continuity_evidence"]:
        admit_continuity(item, p["subject"])
    layers = {v.get("layer") for v in p["validators"] if v.get("required", True)}
    if not {"V1", "V2", "V3"} <= layers:
        raise Blocked("VALIDATOR_UNAVAILABLE", "all three validation layers must be declared")
    value = digest(p)
    return FrozenPacket(json.dumps(p, sort_keys=True, ensure_ascii=False, allow_nan=False), value)


def verify_retry(packet: FrozenPacket, proposed: Mapping[str, Any]) -> None:
    if digest(proposed) != packet.semantic_hash:
        raise Blocked("SPEC_UNRESOLVED", "RETRY changed semantics; explicit REVISE is required")


def classify_result(report: list[dict[str, Any]], required: list[dict[str, Any]],
                    blockers: list[str] | None = None) -> str:
    if blockers:
        return "BLOCKED"
    by_id = {r["validator_id"]: r for r in report}
    if len(by_id) != len(report) or not {"V1", "V2", "V3"} <= {v["layer"] for v in required if v.get("required", True)}:
        return "BLOCKED"
    declared = {v["id"] for v in required}
    if len(declared) != len(required) or set(by_id) - declared:
        return "BLOCKED"
    active = []
    for spec in required:
        row = by_id.get(spec["id"])
        if row is None and not spec.get("required", True):
            continue
        if row is None or row.get("layer") != spec["layer"]:
            return "BLOCKED"
        outcome = row.get("outcome")
        if outcome not in ("PASS", "HARD_FAIL", "OPERATION_FAIL", "LOCAL_DEFECT"):
            return "BLOCKED"
        if outcome == "HARD_FAIL" and (row["layer"] != "V1" or row.get("reason_code") not in HARD_REASONS):
            return "BLOCKED"
        if outcome == "OPERATION_FAIL" and row["layer"] != "V2":
            return "BLOCKED"
        if outcome == "LOCAL_DEFECT" and row["layer"] not in ("V1", "V3"):
            return "BLOCKED"
        active.append(outcome)
    for outcome, result in (("HARD_FAIL", "HARD_RESET"), ("OPERATION_FAIL", "RETRY_REQUIRED"), ("LOCAL_DEFECT", "REFINE_ELIGIBLE")):
        if outcome in active:
            return result
    return "ACCEPT"


def recovery_action(classification: str, packet: FrozenPacket, state: dict[str, Any], attempt_index: int) -> str:
    """Only the first sample may auto-retry, and a pack may narrow that permission to zero."""
    permitted = packet.data["retry_policy"].get("automatic_hard_reset", 0)
    if permitted not in (0, 1):
        raise Blocked("SPEC_UNRESOLVED", "automatic retry cap exceeds one")
    if classification == "HARD_RESET" and permitted == 1 and attempt_index == 1 and state["hard_reset_auto_retry_count"] == 0:
        state["hard_reset_auto_retry_count"] = 1
        state["retry_count"] += 1
        return "FRESH_RETRY_ONCE"
    return "NONE"


def accept_master(packet: FrozenPacket, candidate: dict[str, Any], classification: str,
                  validated_sha256: str, hooks_complete: bool) -> dict[str, Any]:
    p = packet.data
    if classification != "ACCEPT" or not hooks_complete:
        raise Blocked("GATE_NOT_SATISFIED")
    if p["output_kind"] in ("PREVIEW", "DIAGNOSTIC") or candidate.get("kind") != "CLEAN_MASTER_CANDIDATE":
        raise Blocked("PROVENANCE_UNVERIFIED", "accepted preview/diagnostic is not a clean master")
    if (not re.fullmatch(r"[0-9a-f]{64}", candidate.get("sha256", ""))
            or candidate["sha256"] != validated_sha256 or candidate.get("packet_hash") != packet.semantic_hash):
        raise Blocked("PROVENANCE_UNVERIFIED", "candidate changed after validation")
    return {**copy.deepcopy(candidate), "kind": "ACCEPTED_CLEAN_MASTER", "classification": "ACCEPT",
            "subject": p["subject"], "packet_hash": packet.semantic_hash, "provenance_verified": True}


def admit_continuity(master: Mapping[str, Any], subject: Mapping[str, Any]) -> dict[str, Any]:
    if (master.get("kind") != "ACCEPTED_CLEAN_MASTER" or master.get("classification") != "ACCEPT"
            or master.get("provenance_verified") is not True or not master.get("sha256") or not master.get("packet_hash")
            or master.get("subject") != dict(subject)):
        raise Blocked("PROVENANCE_UNVERIFIED", "continuity requires same-subject, same-revision accepted master")
    return copy.deepcopy(dict(master))


def assert_materialized(packet: FrozenPacket, receipts: Mapping[str, Mapping[str, Any]],
                        supported_roles: set[str], *, simulation: bool = False) -> None:
    p = packet.data
    evidence = p["canonical_evidence"] + p["external_evidence"] + p["continuity_evidence"]
    if p.get("edit_target"):
        evidence = evidence + [p["edit_target"]]
    if p.get("preview_reference"):
        evidence = evidence + [p["preview_reference"]]
    for item in evidence:
        receipt = receipts.get(item["id"], {})
        if receipt.get("usable") is not True or not receipt.get("handle") or not receipt.get("sha256"):
            raise Blocked("TRANSPORT_UNAVAILABLE", f"unmaterialized asset {item['id']}")
        if (receipt.get("simulation") or item.get("simulation")) and not simulation:
            raise Blocked("TRANSPORT_UNAVAILABLE", "fixture receipt cannot enter live generation")
        if item.get("sha256") and item["sha256"] != receipt["sha256"]:
            raise Blocked("PROVENANCE_UNVERIFIED", "transport byte identity changed")
        if not set(item.get("roles", [])) <= supported_roles:
            raise Blocked("BACKEND_CAPABILITY_UNAVAILABLE", "cannot preserve reference roles")


def run_hook(stage: str, hook: Mapping[str, Any], artifact: bytes | None,
             registry: Mapping[str, Callable[[bytes | None], bytes | None]]) -> bytes | None:
    if stage not in HOOK_STAGES or hook.get("stage") != stage or hook["id"] not in registry:
        raise Blocked("REQUIRED_HOOK_FAILED", "missing stage-compatible authorized hook")
    try:
        result = registry[hook["id"]](artifact)
    except Exception as exc:
        raise Blocked("REQUIRED_HOOK_FAILED", hook["id"]) from exc
    if stage == "POST_VALIDATION" and result != artifact:
        raise Blocked("REQUIRED_HOOK_FAILED", "post-validation mutation requires new validation")
    if (artifact is not None and not isinstance(result, bytes)) or (result is not None and not isinstance(result, bytes)):
        raise Blocked("REQUIRED_HOOK_FAILED", "hook did not return artifact bytes")
    return result


def import_session(source: Mapping[str, Any], subject: Mapping[str, Any], fields: list[str],
                   *, authorized: bool = False) -> dict[str, Any]:
    allowed = {"shot_registry", "selected_shot", "series_lock", "target_ratio", "accepted_clean_master", "continuity_auxiliaries"}
    if not authorized or not set(fields) <= allowed or source.get("current_subject") != dict(subject):
        raise Blocked("PROVENANCE_UNVERIFIED", "explicit scoped, matching-subject import required")
    state = new_session(subject)
    for field in fields:
        state[field] = copy.deepcopy(source[field])
    if state["selected_shot"] is not None and state["selected_shot"] not in state["shot_registry"]:
        raise Blocked("SPEC_UNRESOLVED", "import selected shot with its registry")
    for master in state["continuity_auxiliaries"] + ([state["accepted_clean_master"]] if state["accepted_clean_master"] else []):
        admit_continuity(master, subject)
    state["session_import"] = {"imported_fields": fields, "provenance_verified": True}
    return state


def prompt_handoff(subject: Mapping[str, Any], effective_spec: Mapping[str, Any],
                   shots: Mapping[str, Any], series_lock: Mapping[str, Any]) -> dict[str, Any]:
    """Compile a metadata-only handoff. No pack references, image I/O, or clean-master mutation."""
    if not subject.get("id") or not effective_spec:
        raise Blocked("SPEC_UNRESOLVED")
    return {"mode": "PROMPT", "subject": copy.deepcopy(dict(subject)),
            "effective_spec": copy.deepcopy(dict(effective_spec)), "shot_registry": copy.deepcopy(dict(shots)),
            "series_lock": copy.deepcopy(dict(series_lock)), "status": "SPEC_COMPILED",
            "generation_executed": False, "canonical_transport_performed": False}
