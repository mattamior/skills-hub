#!/usr/bin/env python3
"""Deterministic Canon contract checks. No network, image generation, or hook loading.

These helpers validate declarations and receipts, not visual identity. A successful
unit test or DRY_RUN is never evidence that a real image or transport was accepted.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMAS = Path(__file__).resolve().parents[1] / "schemas"
ROLES = ("PROTECTED_CANONICAL", "EDIT_TARGET", "PREVIEW_SHOT_REFERENCE",
         "ACCEPTED_CONTINUITY", "EXPLICIT_EXTERNAL_ROLE", "ORIGINAL_PROMPT_REFERENCE")
STAGES = ("PRE_GENERATION", "POST_GENERATION", "PRE_VALIDATION", "POST_VALIDATION", "PRE_DELIVERY")
HARD_REASONS = frozenset({"WRONG_SUBJECT_IDENTITY", "MAJOR_STRUCTURAL_DRIFT",
    "MAJOR_ANATOMY_OR_GEOMETRY_FAILURE", "EXTERNAL_IDENTITY_CONTAMINATION"})
EXTERNAL_ROLES = frozenset({"POSE", "CAMERA", "COMPOSITION", "LIGHTING", "WARDROBE",
    "ENVIRONMENT", "OBJECT", "SECONDARY_SUBJECT", "NON_HUMAN_SUBJECT", "ORIGINAL_PROMPT_REFERENCE"})


class ContractError(ValueError):
    """A contract dependency is unresolved; callers must not sample around it."""


def canonical_bytes(value: Any) -> bytes:
    """Canon JSON v1: UTF-8, sorted object keys, ordered arrays, finite numbers.

    This is an explicitly versioned Python serialization, not an RFC 8785 claim.
    """
    def check(item: Any) -> None:
        if isinstance(item, dict):
            if any(not isinstance(k, str) for k in item):
                raise ContractError("SPEC_UNRESOLVED: object keys must be strings")
            for v in item.values():
                check(v)
        elif isinstance(item, list):
            for v in item:
                check(v)
        elif item is not None and type(item) not in (str, int, float, bool):
            raise ContractError("SPEC_UNRESOLVED: not a JSON value")
    check(value)
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (ValueError, UnicodeError) as exc:
        raise ContractError("SPEC_UNRESOLVED: non-finite or invalid JSON") from exc


def load_json(text: str) -> Any:
    """Reject duplicate object keys and non-finite JSON constants before schema checks."""
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ContractError("SPEC_UNRESOLVED: duplicate JSON key")
            out[key] = value
        return out
    def constant(_):
        raise ContractError("SPEC_UNRESOLVED: non-finite JSON constant")
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate(kind: str, value: Any) -> None:
    """Use only the bundled schemas; never fetch a schema named by input data."""
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError as exc:
        raise ContractError("VALIDATOR_UNAVAILABLE: install jsonschema") from exc
    available = {p.stem.removesuffix(".schema"): json.loads(p.read_text())
                 for p in SCHEMAS.glob("*.schema.json")}
    if kind not in available or kind == "contracts":
        raise ContractError("SPEC_UNRESOLVED: unknown schema")
    registry = Registry().with_resources((s["$id"], Resource.from_contents(s))
                                         for s in available.values())
    canonical_bytes(value)
    errors = list(Draft202012Validator(available[kind], registry=registry).iter_errors(value))
    if errors:
        path = "/".join(map(str, errors[0].absolute_path)) or "/"
        raise ContractError(f"SPEC_UNRESOLVED: {kind} {path}: {errors[0].message}")


def index_unique(rows: list[dict], label: str) -> dict[str, dict]:
    result = {r["id"]: r for r in rows}
    if len(result) != len(rows):
        raise ContractError(f"SPEC_UNRESOLVED: duplicate {label} id")
    return result


def validate_pack(pack: dict) -> None:
    validate("subject-pack", pack)
    groups = index_unique(pack["canon"]["invariant_groups"], "invariant")
    refs = index_unique(pack["references"]["inventory"], "reference")
    index_unique(pack["references"]["profiles"], "profile")
    index_unique(pack["calibration"]["profiles"], "calibration")
    index_unique(pack["postprocess"]["hooks"], "hook")
    def known(items: list, inventory: dict, label: str) -> None:
        if set(items) - inventory.keys():
            raise ContractError(f"SPEC_UNRESOLVED: unknown {label}")
    for r in refs.values():
        # v0.1 prose fixtures used visible_regions as group ids; covers is explicit v1.
        known(r.get("covers", r["visible_regions"]), groups, "coverage group")
        if r["authority"] == "APPROVED_CALIBRATION" and not r.get("approval"):
            raise ContractError("PROVENANCE_UNVERIFIED: calibration approval missing")
    for p in pack["references"]["profiles"]:
        known(p["require"]["invariant_groups"], groups, "profile group")
        known(p["require"].get("assets", []) + p["prefer_assets"], refs, "profile asset")
    for c in pack["calibration"]["profiles"]:
        known(c["authority_assets"], refs, "calibration asset")
    known(pack["references"]["bootstrap_policy"].get("required_assets", []), refs, "bootstrap asset")
    for kind in ("identity", "structure", "local_quality"):
        index_unique(pack["validators"][kind], kind + " validator")
    known([g for w in pack["canon"]["written_authority"] for g in w["scope"]], groups, "written scope")
    for h in pack["postprocess"]["hooks"]:
        known(h.get("deferred_invariant_groups", []), groups, "deferred invariant")


def resolve_route(task: dict, state: dict) -> str:
    """Resolve normalized task intent, not ambiguous natural language guesses."""
    if task.get("calibration"):
        return "CALIBRATION"
    shot = task.get("shot_id")
    if shot:
        if shot not in state.get("shot_registry", {}):
            raise ContractError("SPEC_UNRESOLVED: unknown shot")
        return "EXISTING_SERIES_SHOT"
    if task.get("current_operation"):
        if state.get("selected_shot") not in state.get("shot_registry", {}):
            raise ContractError("SPEC_UNRESOLVED: no selected shot")
        return "CURRENT_SHOT_OPERATION"
    if task.get("preview"):
        return "PREVIEW_ONLY"
    if task.get("series"):
        return "SERIES"
    return "STANDALONE_SHOT"


def resolve_image_role(eligible: list[str]) -> str:
    if set(eligible) - set(ROLES):
        raise ContractError("SPEC_UNRESOLVED: unknown image role")
    return next((r for r in ROLES if r in eligible), "ORIGINAL_PROMPT_REFERENCE")


def external_roles(explicit: list[str] | None, prompt_scopes: list[str],
                   declared_roles: dict | None = None) -> list[str]:
    """Explicit scope wins; extension meanings must be declared by the caller pack."""
    roles = explicit if explicit is not None else prompt_scopes
    declared = declared_roles or {}
    if any(not isinstance(d, dict) or not isinstance(d.get("allowed_influence"), list)
           or any(not isinstance(x, str) or x.startswith(("primary_subject.identity", "primary_subject.structural_invariants"))
                  for x in d.get("allowed_influence", [])) for d in declared.values()):
        raise ContractError("SPEC_UNRESOLVED: extension cannot authorize primary identity")
    if any(not re.fullmatch(r"extension:[a-z0-9]+(?:-[a-z0-9]+)*", r) for r in declared):
        raise ContractError("SPEC_UNRESOLVED: invalid extension role declaration")
    if (not roles or set(roles) - EXTERNAL_ROLES - declared.keys()
            or "ORIGINAL_PROMPT_REFERENCE" in roles):
        raise ContractError("SPEC_UNRESOLVED: external influence not scoped")
    return list(dict.fromkeys(roles))


def select_evidence(pack: dict, shot: dict, required: list[str]) -> dict:
    """Exact minimum cover for compact packs; preserve mandatory profile assets."""
    validate_pack(pack)
    attributes = {**shot, "views": shot.get("view", shot.get("views"))}
    profiles = [p for p in pack["references"]["profiles"]
                if all(attributes.get(k) in v for k, v in p["match"].items())]
    if shot.get("reference_profile"):
        profiles = [p for p in profiles if p["id"] == shot["reference_profile"] or p.get("kind") == "SUPPLEMENT"]
    if (pack.get("runtime_policy", {}).get("profile_selection") == "SINGLE_PRIMARY"
            and sum(p.get("kind", "PRIMARY") == "PRIMARY" for p in profiles) > 1):
        raise ContractError("SPEC_UNRESOLVED: select one Primary Profile")
    if not any(p.get("kind", "PRIMARY") == "PRIMARY" for p in profiles):
        raise ContractError("CANONICAL_EVIDENCE_UNAVAILABLE: no matching profile")
    need, mandatory, preferred = set(required), set(), set()
    mandatory_order = []
    profiles.sort(key=lambda p: (p.get("kind", "PRIMARY") != "PRIMARY", p["id"]))
    for p in profiles:
        need.update(p["require"]["invariant_groups"])
        mandatory.update(p["require"].get("assets", []))
        mandatory_order.extend(r for r in p["require"].get("assets", []) if r not in mandatory_order)
        preferred.update(p["prefer_assets"])
    groups = {g["id"] for g in pack["canon"]["invariant_groups"]}
    if need - groups or not need:
        raise ContractError("SPEC_UNRESOLVED: invalid required coverage")
    candidates = [r for r in pack["references"]["inventory"]
                  if r["generation_eligible"] and not r["diagnostic_only"]
                  and (need.intersection(r.get("covers", r["visible_regions"])) or r["id"] in mandatory)]
    if mandatory - {r["id"] for r in candidates}:
        raise ContractError("CANONICAL_EVIDENCE_UNAVAILABLE: required asset ineligible")
    # Compact evidence sets are deliberate; never silently approximate a huge search.
    if len(candidates) > 24:
        raise ContractError("SPEC_UNRESOLVED: narrow profiles before minimum-cover search")
    def score(rows: tuple) -> tuple:
        return (-sum(shot.get("views", shot.get("view")) in r["views"] for r in rows),
                -sum(r["id"] in preferred for r in rows),
                -sum(r["authority"] == "CANONICAL_VISUAL" for r in rows),
                sum(len(set(r.get("covers", r["visible_regions"])) - need) for r in rows),
                tuple(sorted(r["id"] for r in rows)))
    for n in range(max(1, len(mandatory)), len(candidates) + 1):
        best, best_score = None, None
        for rows in itertools.combinations(candidates, n):
            if not mandatory.issubset({r["id"] for r in rows}):
                continue
            covered = set().union(*(set(r.get("covers", r["visible_regions"])) for r in rows))
            if need.issubset(covered):
                row_score = score(rows)
                if best_score is None or row_score < best_score:
                    best, best_score = rows, row_score
        if best is not None:
            chosen = sorted(best, key=lambda r: (mandatory_order.index(r["id"]) if r["id"] in mandatory_order else len(mandatory_order), r["id"]))
            return {"required_invariant_groups": sorted(need), "matched_profiles": [p["id"] for p in profiles],
                    "canonical_evidence": copy.deepcopy(chosen), "uncovered": []}
    raise ContractError("CANONICAL_EVIDENCE_UNAVAILABLE: uncovered invariants")


def validate_packet(packet: dict) -> None:
    validate("generation-packet", packet)
    validators = index_unique(packet["validators"], "validator")
    if {v["layer"] for v in validators.values()} != {"V1", "V2", "V3"}:
        raise ContractError("VALIDATOR_UNAVAILABLE: all three layers are required")
    if any(g["status"] not in ("PASSED", "NOT_REQUIRED") for g in packet["required_gates"]):
        raise ContractError("GATE_NOT_SATISFIED")
    index_unique(packet["required_gates"], "gate")
    for e in packet["canonical_evidence"]:
        if packet["image_roles"].get(e["id"]) != "PROTECTED_CANONICAL":
            raise ContractError("SPEC_UNRESOLVED: canonical image-role binding missing")
        if e["authority"] == "APPROVED_CALIBRATION" and not e.get("approval"):
            raise ContractError("PROVENANCE_UNVERIFIED: calibration approval missing")
        if not e["generation_eligible"] or e["diagnostic_only"]:
            raise ContractError("CANONICAL_EVIDENCE_UNAVAILABLE: diagnostic generation input")
    for e in packet["external_evidence"]:
        external_roles(e["roles"], [], e.get("role_definitions", {}))
        if packet["image_roles"].get(e["id"]) not in ("EXPLICIT_EXTERNAL_ROLE", "ORIGINAL_PROMPT_REFERENCE"):
            raise ContractError("SPEC_UNRESOLVED: external image-role binding missing")
        if any(x.startswith(("primary_subject.identity", "primary_subject.structural_invariants")) for x in e["allowed_influence"]):
            raise ContractError("SPEC_UNRESOLVED: external allowed/denied scope conflict")
        if not {"primary_subject.identity", "primary_subject.structural_invariants"}.issubset(e["denied_influence"]):
            raise ContractError("SPEC_UNRESOLVED: external identity guard missing")
    for e in packet["continuity_evidence"]:
        if packet["image_roles"].get(e["id"]) != "ACCEPTED_CONTINUITY":
            raise ContractError("SPEC_UNRESOLVED: continuity image-role binding missing")
        if e["series_id"] != packet["series_lock"].get("id"):
            raise ContractError("PROVENANCE_UNVERIFIED: wrong continuity series")
        if e["subject_id"] != packet["subject"]["id"] or e["candidate_sha256"] != e["validated_sha256"]:
            raise ContractError("PROVENANCE_UNVERIFIED: incompatible continuity")
    if any(h["stage"] != "PRE_GENERATION" for h in packet["preprocess_hooks"]):
        raise ContractError("SPEC_UNRESOLVED: invalid pre-generation hook stage")
    if any(h["stage"] == "PRE_GENERATION" for h in packet["postprocess_hooks"]):
        raise ContractError("SPEC_UNRESOLVED: pre-generation hook in postprocess channel")
    hooks = packet["preprocess_hooks"] + packet["postprocess_hooks"]
    index_unique(hooks, "hook")
    for key, role in (("edit_target", "EDIT_TARGET"), ("preview_reference", "PREVIEW_SHOT_REFERENCE")):
        image = packet[key]
        if image and packet["image_roles"].get(image["id"]) != role:
            raise ContractError("SPEC_UNRESOLVED: operation image-role binding missing")
    if packet["preview_reference"] and packet["preview_reference"]["shot_id"] != packet["shot"]["id"]:
        raise ContractError("PREVIEW_REFERENCE_UNAVAILABLE: selected shot mismatch")
    if packet["edit_target"] and packet["edit_target"]["provenance"] == "DELIVERY_DERIVATIVE":
        raise ContractError("EDIT_TARGET_UNAVAILABLE: use derivative-only delivery workflow")
    for h in hooks:
        if not h.get("handler") or not h.get("revision"):
            raise ContractError("VALIDATOR_UNAVAILABLE: unresolved hook implementation")
    ids = [r["id"] for channel in ("canonical_evidence", "external_evidence", "continuity_evidence") for r in packet[channel]]
    if len(ids) != len(set(ids)):
        raise ContractError("SPEC_UNRESOLVED: evidence channels overlap")


def freeze(packet: dict) -> dict:
    validate_packet(packet)
    return {"format": "canon-json-v1", "digest": digest(packet), "payload": copy.deepcopy(packet)}


def verify_frozen(envelope: dict) -> dict:
    if set(envelope) != {"format", "digest", "payload"} or envelope["format"] != "canon-json-v1":
        raise ContractError("SPEC_UNRESOLVED: invalid frozen envelope")
    if digest(envelope["payload"]) != envelope["digest"]:
        raise ContractError("SPEC_UNRESOLVED: packet semantics changed; REVISE required")
    validate_packet(envelope["payload"])
    return envelope["payload"]


def retry(envelope: dict, transport: dict) -> dict:
    verify_frozen(envelope)
    if set(transport) - {"seed", "request_id", "attachment_handles"}:
        raise ContractError("SPEC_UNRESOLVED: non-transport retry change")
    return {"packet": copy.deepcopy(envelope), "transport": copy.deepcopy(transport)}


def revise(envelope: dict, changes: dict[str, Any], authorized_paths: list[str]) -> dict:
    payload = copy.deepcopy(verify_frozen(envelope))
    if not changes or set(changes) - set(authorized_paths):
        raise ContractError("SPEC_UNRESOLVED: revision exceeds Principal-authorized fields")
    for path, value in changes.items():
        if not path.startswith("/") or "~" in path:
            raise ContractError("SPEC_UNRESOLVED: use exact simple object paths")
        keys = path[1:].split("/")
        target = payload
        for key in keys[:-1]:
            if not isinstance(target, dict) or key not in target:
                raise ContractError("SPEC_UNRESOLVED: revision path does not exist")
            target = target[key]
        if not isinstance(target, dict) or keys[-1] not in target:
            raise ContractError("SPEC_UNRESOLVED: revision path does not exist")
        target[keys[-1]] = copy.deepcopy(value)
    if payload["shot"]["revision"] == envelope["payload"]["shot"]["revision"]:
        raise ContractError("SPEC_UNRESOLVED: revision identifier must advance")
    return freeze(payload)


def classify(packet: dict, report: dict, candidate_sha256: str) -> str:
    """Aggregate supplied inspection evidence; never infer a visual PASS."""
    validate_packet(packet)
    if not isinstance(report, dict) or not isinstance(candidate_sha256, str):
        return "BLOCKED"
    if (report.get("candidate_sha256") != candidate_sha256
            or report.get("packet_digest") != digest(packet)
            or report.get("dependencies") != "SATISFIED"
            or not re.fullmatch(r"[0-9a-f]{64}", candidate_sha256)):
        return "BLOCKED"
    if report.get("phase", "FINAL_VALIDATION") != "FINAL_VALIDATION":
        return "BLOCKED"
    rows = report.get("checks", [])
    if not isinstance(rows, list) or any(not isinstance(r, dict) or not isinstance(r.get("id"), str) for r in rows):
        return "BLOCKED"
    if len({r.get("id") for r in rows}) != len(rows):
        return "BLOCKED"
    actual = {r.get("id"): r for r in rows}
    for v in packet["validators"]:
        if v["id"] not in actual or actual[v["id"]].get("layer") != v["layer"]:
            return "BLOCKED"
    required_hooks = [h for h in packet["preprocess_hooks"] + packet["postprocess_hooks"]
                      if packet["output_kind"] in h["required_for"] and h["stage"] != "PRE_DELIVERY"]
    if not isinstance(report.get("hooks", {}), dict):
        return "BLOCKED"
    if any(report.get("hooks", {}).get(h["id"]) != "PASS" for h in required_hooks):
        return "BLOCKED"
    if set(actual) != {v["id"] for v in packet["validators"]}:
        return "BLOCKED"
    for row in rows:
        outcome, layer = row.get("outcome"), row.get("layer")
        if outcome not in {"PASS", "HARD_FAIL", "OPERATION_FAIL", "LOCAL_DEFECT"}:
            return "BLOCKED"
        if outcome == "HARD_FAIL" and (layer != "V1" or row.get("reason") not in HARD_REASONS):
            return "BLOCKED"
        if outcome == "OPERATION_FAIL" and layer != "V2":
            return "BLOCKED"
        if outcome == "LOCAL_DEFECT" and layer not in {"V1", "V3"}:
            return "BLOCKED"
    outcomes = {r["outcome"] for r in rows}
    for outcome, result in (("HARD_FAIL", "HARD_RESET"), ("OPERATION_FAIL", "RETRY_REQUIRED"),
                            ("LOCAL_DEFECT", "REFINE_ELIGIBLE")):
        if outcome in outcomes:
            return result
    return "ACCEPT"


def recovery_action(classification: str, auto_count: int, retry_policy: dict) -> str:
    if classification not in {"ACCEPT", "HARD_RESET", "RETRY_REQUIRED", "REFINE_ELIGIBLE", "BLOCKED"}:
        raise ContractError("SPEC_UNRESOLVED: unknown result classification")
    validate_retry = retry_policy.get("automatic_hard_reset_limit")
    if type(auto_count) is not int or auto_count not in (0, 1) or type(validate_retry) is not int or validate_retry not in (0, 1):
        raise ContractError("SPEC_UNRESOLVED: invalid automatic retry budget")
    return ("FRESH_RETRY_ONCE" if classification == "HARD_RESET" and auto_count == 0
            and validate_retry == 1 and retry_policy.get("eligible") is True else "NONE")


def admit_continuity(master: dict, subject_id: str, series_id: str) -> bool:
    try:
        # Use a wrapper schema fragment through a packet-independent bundled validator.
        from jsonschema import Draft202012Validator, ValidationError
    except ImportError:
        return False
    try:
        canonical_bytes(master)
        schema = json.loads((SCHEMAS / "contracts.schema.json").read_text())
        schema["$ref"] = "#/$defs/master"
        Draft202012Validator(schema).validate(master)
    except (ValueError, OSError, ValidationError):
        return False
    # Valid declarations still require caller-verified runtime provenance.
    return (master["subject_id"] == subject_id and master["series_id"] == series_id
            and master["candidate_sha256"] == master["validated_sha256"])


def new_state() -> dict:
    """Fresh session namespace; never accepts a previous-session state implicitly."""
    schema = json.loads((SCHEMAS / "contracts.schema.json").read_text())
    keys = schema["$defs"]["runtimeState"]["properties"]
    state = {key: None for key in keys}
    state.update(series_lock={}, shot_registry={}, external_reference_role_map={},
                 identity_gate={"status": "OPEN"}, preview_gate={"status": "OPEN"},
                 external_reference_mode="NONE", continuity_auxiliaries=[], retry_count=0,
                 hard_reset_auto_retry_count=0)
    validate("runtime-state", state)
    return state


def verify_transport(envelope: dict, receipts: list[dict]) -> None:
    """Verify adapter receipts; self-reported receipts do not prove image transport."""
    packet = verify_frozen(envelope)
    required = {e["id"]: e for key in ("canonical_evidence", "external_evidence") for e in packet[key]}
    required.update({e["id"]: {"sha256": e["candidate_sha256"]} for e in packet["continuity_evidence"]})
    for key in ("edit_target", "preview_reference"):
        if packet[key]:
            required[packet[key]["id"]] = packet[key]
    actual = index_unique(receipts, "transport receipt")
    if set(actual) != set(required):
        raise ContractError("REFERENCE_TRANSPORT_UNAVAILABLE: receipt set differs from packet")
    for rid, item in required.items():
        receipt = actual[rid]
        allowed_hashes = {item.get("sha256"), *(t["sha256"] for t in item.get("transports", []))} - {None}
        if (not allowed_hashes or receipt.get("sha256") not in allowed_hashes
                or receipt.get("packet_digest") != envelope["digest"]
                or receipt.get("materialized") is not True
                or receipt.get("attached") is not True or not receipt.get("handle")):
            raise ContractError("REFERENCE_TRANSPORT_UNAVAILABLE: missing or mismatched actual attachment")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate-pack", "validate-spec", "freeze", "verify", "compare"))
    parser.add_argument("file", type=Path)
    parser.add_argument("other", nargs="?", type=Path)
    args = parser.parse_args()
    try:
        data = load_json(args.file.read_text(encoding="utf-8"))
        if args.command == "validate-pack":
            validate_pack(data); result = {"valid": True, "scope": "declarations-only"}
        elif args.command == "validate-spec":
            validate("generation-spec", data); result = {"valid": True, "scope": "prompt-only"}
        elif args.command == "freeze":
            result = freeze(data)
        elif args.command == "verify":
            verify_frozen(data); result = {"valid": True, "digest": data["digest"]}
        else:
            if args.other is None:
                raise ContractError("SPEC_UNRESOLVED: compare requires two frozen packets")
            other = load_json(args.other.read_text(encoding="utf-8"))
            verify_frozen(data); verify_frozen(other)
            result = {"equal": data["digest"] == other["digest"]}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("equal", True) else 1
    except (ContractError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
