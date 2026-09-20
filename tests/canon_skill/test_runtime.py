"""Executable contract regressions. Synthetic receipts/results are NOT visual acceptance."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

import jsonschema
from referencing import Registry, Resource
import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'skills/canon-skill'
spec = importlib.util.spec_from_file_location('canon_contract_runtime', SKILL / 'scripts/contract_runtime.py')
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
VALIDATORS = [{'id': 'core-canon', 'layer': 'V1'}, {'id': 'core-operation', 'layer': 'V2'}, {'id': 'core-quality', 'layer': 'V3'}]


def reports(v1='PASS', v2='PASS', v3='PASS'):
    return [{'validator_id': v['id'], 'layer': v['layer'], 'outcome': o,
             'reason_code': 'WRONG_SUBJECT_IDENTITY' if o == 'HARD_FAIL' else 'OBSERVED_DEFECT'}
            for v, o in zip(VALIDATORS, (v1, v2, v3))]


def base_packet():
    return {'subject': {'id': 'test-subject', 'pack_revision': 'test-revision'},
            'route': 'STANDALONE_SHOT', 'operation': 'GENERATE', 'effective_spec': {'description': 'test shot'},
            'series_lock': {}, 'shot': {'id': 'S1', 'view': 'front', 'framing': 'close-up'},
            'canonical_evidence': [{'id': 'canonical-front', 'authority': 'CANONICAL_VISUAL'}],
            'external_evidence': [], 'continuity_evidence': [], 'preserve_constraints': [], 'risk_guards': [],
            'preprocess_hooks': [], 'postprocess_hooks': [], 'validators': copy.deepcopy(VALIDATORS),
            'retry_policy': {'automatic_hard_reset': 1}, 'delivery_policy': {}, 'output_kind': 'FINAL'}


def candidate(packet):
    return {'id': 'synthetic-result', 'sha256': hashlib.sha256(b'synthetic test bytes').hexdigest(),
            'packet_hash': packet.semantic_hash, 'kind': 'CLEAN_MASTER_CANDIDATE', 'simulation': True}


def master():
    packet = r.freeze_packet(base_packet())
    c = candidate(packet)
    return r.accept_master(packet, c, 'ACCEPT', c['sha256'], True)


class Contracts(unittest.TestCase):
    def test_fresh_state_has_no_transient_carryover(self):
        old = r.new_session({'id': 'x', 'pack_revision': '1'})
        old['shot_registry']['B3'] = {'id': 'B3'}
        fresh = r.new_session(old['current_subject'])
        self.assertEqual(fresh['shot_registry'], {})
        self.assertIsNone(fresh['generation_packet'])
        self.assertEqual(fresh['identity_gate']['status'], 'OPEN')

    def test_all_six_routes(self):
        s = r.new_session(); s['shot_registry'] = {'B3': {}}; s['selected_shot'] = 'B3'
        pairs = [({'calibration': True}, 'CALIBRATION'), ({'current_operation': 'RETRY'}, 'CURRENT_SHOT_OPERATION'),
                 ({'shot_id': 'B3', 'preview': True}, 'EXISTING_SERIES_SHOT'), ({'preview': True}, 'PREVIEW_ONLY'),
                 ({'series': True}, 'SERIES'), ({}, 'STANDALONE_SHOT')]
        for intent, expected in pairs:
            with self.subTest(expected=expected): self.assertEqual(r.resolve_route(intent, s), expected)

    def test_unknown_or_unselected_shot_blocks(self):
        for task in ({'shot_id': 'unknown'}, {'current_operation': 'RETRY'}):
            with self.subTest(task=task), self.assertRaises(r.Blocked): r.resolve_route(task, r.new_session())

    def test_named_target_beats_implicit_current(self):
        s = r.new_session(); s['shot_registry'] = {'B3': {}, 'C2': {}}; s['selected_shot'] = 'C2'
        self.assertEqual(r.resolve_route({'shot_id': 'B3', 'current_operation': 'EDIT'}, s), 'EXISTING_SERIES_SHOT')

    def test_all_image_precedence_conflicts(self):
        for index, expected in enumerate(r.ROLES):
            with self.subTest(expected=expected):
                result = r.resolve_image_roles([{'id': 'x'}], {'x'} if index == 0 else set(),
                    'x' if index <= 1 else None, {'x'} if index <= 2 else set(),
                    {'x'} if index <= 3 else set(), {'x': ['LIGHTING']} if index <= 4 else {})
                self.assertEqual(result[0]['primary_role'], expected)

    def test_edit_target_is_not_routed_as_reference(self):
        bound = r.resolve_image_roles([{'id': 'x'}], set(), edit_id='x', explicit={'x': ['POSE']})
        self.assertEqual(r.route_external(bound), [])

    def test_preview_selection_is_not_upscale(self):
        bound = r.resolve_image_roles([{'id': 'B3-preview'}], set(), preview_ids={'B3-preview'})
        self.assertEqual(bound[0]['primary_role'], 'PREVIEW_SHOT_REFERENCE')
        self.assertEqual(r.route_external(bound), [])

    def test_missing_target_or_reference_map_blocks(self):
        for args in ({'edit_id': 'missing'}, {'explicit': {'missing': ['POSE']}}):
            with self.subTest(args=args), self.assertRaises(r.Blocked): r.resolve_image_roles([], set(), **args)

    def test_duplicate_image_binding_blocks(self):
        with self.assertRaises(r.Blocked): r.resolve_image_roles([{'id': 'x'}, {'id': 'x'}], set())

    def test_explicit_role_removes_fallback(self):
        bound = r.resolve_image_roles([{'id': 'x'}], set(), explicit={'x': ['LIGHTING']})
        plan = r.route_external(bound, ['POSE', 'COMPOSITION'])
        self.assertEqual(plan[0]['roles'], ['LIGHTING'])
        self.assertIn('NO_EXTERNAL_IDENTITY_TRANSFER', plan[0]['risk_guards'])

    def test_unscoped_reference_blocks(self):
        bound = r.resolve_image_roles([{'id': 'x'}], set())
        with self.assertRaises(r.Blocked): r.route_external(bound)

    def test_external_primary_identity_is_never_a_role(self):
        bound = r.resolve_image_roles([{'id': 'x'}], set(), explicit={'x': ['IDENTITY']})
        with self.assertRaises(r.Blocked): r.route_external(bound)

    def test_nonhuman_role_is_backward_compatible(self):
        bound = r.resolve_image_roles([{'id': 'x'}], set(), explicit={'x': ['NON_HUMAN_SUBJECT']})
        self.assertEqual(r.route_external(bound)[0]['roles'], ['NON_HUMAN_SUBJECT'])

    def test_prompt_compiler_is_metadata_only(self):
        handoff = r.prompt_handoff({'id': 'x'}, {'camera': 'front'}, {'B3': {'view': 'front'}}, {})
        self.assertFalse(handoff['generation_executed'])
        self.assertFalse(handoff['canonical_transport_performed'])
        self.assertNotIn('canonical_evidence', handoff)
        self.assertNotIn('accepted_clean_master', handoff)

    def test_packet_is_detached_and_retry_is_semantic(self):
        source = base_packet(); frozen = r.freeze_packet(source)
        source['shot']['view'] = 'rear'
        self.assertEqual(frozen.data['shot']['view'], 'front')
        copy_out = frozen.data; copy_out['shot']['view'] = 'side'
        self.assertEqual(frozen.data['shot']['view'], 'front')
        r.verify_retry(frozen, frozen.data)
        with self.assertRaises(r.Blocked): r.verify_retry(frozen, source)

    def test_every_semantic_packet_field_is_frozen(self):
        frozen = r.freeze_packet(base_packet())
        for key in r.PACKET_FIELDS:
            changed = frozen.data; changed[key] = {'changed': True}
            with self.subTest(field=key), self.assertRaises(r.Blocked): r.verify_retry(frozen, changed)

    def test_empty_packet_or_missing_canon_blocks(self):
        for change in ({}, {'canonical_evidence': []}, {'validators': []}):
            p = base_packet() if change else {}; p.update(change)
            with self.subTest(change=change), self.assertRaises(r.Blocked): r.freeze_packet(p)

    def test_nonfinite_packet_values_block(self):
        with self.assertRaises(r.Blocked): r.digest({'value': float('nan')})

    def test_gate_binds_exact_spec_scope(self):
        p = base_packet()
        scope = r.digest({k: p[k] for k in ('subject', 'effective_spec', 'series_lock', 'shot', 'output_kind')})
        p['gates'] = [{'required': True, 'status': 'PASSED', 'evidence_id': 'approval-1', 'scope_hash': scope}]
        r.freeze_packet(p)
        p['shot']['view'] = 'rear'
        with self.assertRaises(r.Blocked): r.freeze_packet(p)

    def test_five_classes_and_mixed_failure_precedence(self):
        cases = [(reports(), [], 'ACCEPT'), (reports('HARD_FAIL'), [], 'HARD_RESET'),
                 (reports(v2='OPERATION_FAIL'), [], 'RETRY_REQUIRED'), (reports(v3='LOCAL_DEFECT'), [], 'REFINE_ELIGIBLE'),
                 (reports('LOCAL_DEFECT'), [], 'REFINE_ELIGIBLE'), (reports(), ['missing'], 'BLOCKED'),
                 (reports('HARD_FAIL', 'OPERATION_FAIL', 'LOCAL_DEFECT'), [], 'HARD_RESET'),
                 (reports(v2='OPERATION_FAIL', v3='LOCAL_DEFECT'), [], 'RETRY_REQUIRED')]
        for report, blockers, expected in cases:
            with self.subTest(expected=expected): self.assertEqual(r.classify_result(report, VALIDATORS, blockers), expected)

    def test_missing_validator_is_not_vacuous_accept(self):
        for report in ([], reports()[:-1]):
            with self.subTest(report=report): self.assertEqual(r.classify_result(report, VALIDATORS), 'BLOCKED')

    def test_invalid_layer_outcomes_block(self):
        rows = reports(); rows[2]['outcome'] = 'HARD_FAIL'; rows[2]['reason_code'] = 'WRONG_SUBJECT_IDENTITY'
        self.assertEqual(r.classify_result(rows, VALIDATORS), 'BLOCKED')
        rows = reports('HARD_FAIL'); rows[0]['reason_code'] = 'CAMERA_NONCOMPLIANCE'
        self.assertEqual(r.classify_result(rows, VALIDATORS), 'BLOCKED')

    def test_optional_observed_failure_is_not_silently_discarded(self):
        validators = VALIDATORS + [{'id': 'extra', 'layer': 'V1', 'required': False}]
        rows = reports() + [{'validator_id': 'extra', 'layer': 'V1', 'outcome': 'HARD_FAIL', 'reason_code': 'MAJOR_STRUCTURAL_DRIFT'}]
        self.assertEqual(r.classify_result(rows, validators), 'HARD_RESET')

    def test_second_attempt_always_stops_automatic_execution(self):
        packet = r.freeze_packet(base_packet())
        for outcome in ('ACCEPT', 'HARD_RESET', 'RETRY_REQUIRED', 'REFINE_ELIGIBLE', 'BLOCKED'):
            with self.subTest(outcome=outcome):
                state = r.new_session()
                self.assertEqual(r.recovery_action('HARD_RESET', packet, state, 1), 'FRESH_RETRY_ONCE')
                self.assertEqual(r.recovery_action(outcome, packet, state, 2), 'NONE')
                self.assertEqual(state['hard_reset_auto_retry_count'], 1)

    def test_only_hard_reset_may_automatically_retry(self):
        packet = r.freeze_packet(base_packet())
        for outcome in ('ACCEPT', 'RETRY_REQUIRED', 'REFINE_ELIGIBLE', 'BLOCKED'):
            with self.subTest(outcome=outcome): self.assertEqual(r.recovery_action(outcome, packet, r.new_session(), 1), 'NONE')

    def test_pack_can_disable_but_not_expand_automatic_retry(self):
        p = base_packet(); p['route'] = 'CALIBRATION'; p['retry_policy']['automatic_hard_reset'] = 0
        self.assertEqual(r.recovery_action('HARD_RESET', r.freeze_packet(p), r.new_session(), 1), 'NONE')
        p['retry_policy']['automatic_hard_reset'] = 2
        with self.assertRaises(r.Blocked): r.freeze_packet(p)

    def test_accept_requires_same_post_hook_bytes(self):
        packet = r.freeze_packet(base_packet()); c = candidate(packet)
        for classification, checksum, hooks in [('REFINE_ELIGIBLE', c['sha256'], True), ('ACCEPT', 'different', True), ('ACCEPT', c['sha256'], False)]:
            with self.subTest(classification=classification, checksum=checksum, hooks=hooks), self.assertRaises(r.Blocked):
                r.accept_master(packet, c, classification, checksum, hooks)

    def test_accepting_preview_does_not_create_master(self):
        for kind in ('PREVIEW', 'DIAGNOSTIC'):
            p = base_packet(); p['output_kind'] = kind; packet = r.freeze_packet(p); c = candidate(packet)
            with self.subTest(kind=kind), self.assertRaises(r.Blocked): r.accept_master(packet, c, 'ACCEPT', c['sha256'], True)

    def test_master_belongs_to_validated_packet(self):
        packet = r.freeze_packet(base_packet()); c = candidate(packet); c['packet_hash'] = 'another'
        with self.assertRaises(r.Blocked): r.accept_master(packet, c, 'ACCEPT', c['sha256'], True)

    def test_continuity_rejects_every_nonmaster_provenance(self):
        original = master()
        for kind in ('PREVIEW', 'CONSTRUCTION_INTERMEDIATE', 'CLEAN_MASTER_CANDIDATE', 'DELIVERY_DERIVATIVE', 'GENERATED_UNVERIFIED'):
            invalid = {**original, 'kind': kind}
            with self.subTest(kind=kind), self.assertRaises(r.Blocked): r.admit_continuity(invalid, original['subject'])

    def test_continuity_rejects_other_subject_or_pack_revision(self):
        original = master()
        with self.assertRaises(r.Blocked): r.admit_continuity(original, {'id': 'another', 'pack_revision': 'test-revision'})
        with self.assertRaises(r.Blocked): r.admit_continuity(original, {**original['subject'], 'pack_revision': 'new'})

    def test_delivery_derivative_never_reenters_continuity(self):
        original = master(); derivative = {**original, 'id': 'delivery', 'kind': 'DELIVERY_DERIVATIVE', 'source_master_id': original['id']}
        with self.assertRaises(r.Blocked): r.admit_continuity(derivative, original['subject'])

    def test_hooks_must_be_registered_and_postvalidation_is_readonly(self):
        hook = {'id': 'detail', 'stage': 'POST_GENERATION'}
        self.assertEqual(r.run_hook('POST_GENERATION', hook, b'base', {'detail': lambda b: b + b'-finalized'}), b'base-finalized')
        with self.assertRaises(r.Blocked): r.run_hook('POST_GENERATION', hook, b'base', {})
        hook['stage'] = 'POST_VALIDATION'
        with self.assertRaises(r.Blocked): r.run_hook('POST_VALIDATION', hook, b'base', {'detail': lambda b: b + b'-changed'})

    def test_all_hook_stages_are_explicit(self):
        seen = []
        for stage in r.HOOK_STAGES:
            hook = {'id': stage, 'stage': stage}
            def action(data, stage=stage): seen.append(stage); return data
            r.run_hook(stage, hook, b'synthetic', {stage: action})
        self.assertEqual(tuple(seen), r.HOOK_STAGES)

    def test_hook_exceptions_block_instead_of_skipping(self):
        def fail(_): raise RuntimeError('unavailable')
        with self.assertRaises(r.Blocked): r.run_hook('PRE_VALIDATION', {'id': 'x', 'stage': 'PRE_VALIDATION'}, b'base', {'x': fail})

    def test_materialization_and_backend_capabilities(self):
        p = base_packet(); p['external_evidence'] = [{'id': 'external', 'authority': 'ROLE_SCOPED_EXTERNAL_REFERENCE', 'roles': ['POSE']}]
        packet = r.freeze_packet(p)
        with self.assertRaises(r.Blocked): r.assert_materialized(packet, {}, set(r.EXTERNAL))
        receipts = {i: {'usable': True, 'handle': 'sim:'+i, 'sha256': r.digest(i), 'simulation': True} for i in ('canonical-front', 'external')}
        with self.assertRaises(r.Blocked): r.assert_materialized(packet, receipts, set(r.EXTERNAL))
        with self.assertRaises(r.Blocked): r.assert_materialized(packet, receipts, set(), simulation=True)
        r.assert_materialized(packet, receipts, set(r.EXTERNAL), simulation=True)

    def test_import_is_scoped_and_gates_start_fresh(self):
        original = master(); state = r.new_session(original['subject'])
        state['shot_registry'] = {'B3': {'id': 'B3'}}; state['selected_shot'] = 'B3'; state['accepted_clean_master'] = original
        with self.assertRaises(r.Blocked): r.import_session(state, original['subject'], ['shot_registry'])
        imported = r.import_session(state, original['subject'], ['shot_registry', 'selected_shot', 'accepted_clean_master'], authorized=True)
        self.assertEqual(imported['selected_shot'], 'B3'); self.assertEqual(imported['identity_gate']['status'], 'OPEN')
        with self.assertRaises(r.Blocked): r.import_session(state, original['subject'], ['generation_packet'], authorized=True)
        with self.assertRaises(r.Blocked): r.import_session(state, original['subject'], ['selected_shot'], authorized=True)


class PackAndDryRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {p.name: json.loads(p.read_text()) for p in (SKILL/'assets/schemas').glob('*.json')}
        cls.registry = Registry().with_resources((s['$id'], Resource.from_contents(s)) for s in cls.schemas.values())
        cls.packs = {p.stem: yaml.safe_load(p.read_text()) for p in (SKILL/'references/fixtures').glob('*.yaml')}

    def validate(self, name, data):
        schema = self.schemas[name+'.schema.json']
        jsonschema.Draft202012Validator(schema, registry=self.registry).validate(data)

    def test_schema_documents_are_valid(self):
        self.assertEqual(len(self.schemas), 6)
        for name, schema in self.schemas.items():
            with self.subTest(name=name): jsonschema.Draft202012Validator.check_schema(schema)

    def test_three_anonymous_packs_share_one_contract(self):
        self.assertEqual(set(self.packs), {'human','pet','virtual-character'})
        for name, pack in self.packs.items():
            with self.subTest(subject=name): self.validate('subject-pack', pack)

    def test_new_state_and_packet_validate(self):
        self.validate('runtime-state', r.new_session())
        self.validate('generation-packet', r.freeze_packet(base_packet()).data)

    def test_schema_rejects_missing_required_pack_fields(self):
        for field in ('subject','canon','references','calibration','validators','postprocess','delivery'):
            pack = copy.deepcopy(self.packs['pet']); del pack[field]
            with self.subTest(field=field), self.assertRaises(jsonschema.ValidationError): self.validate('subject-pack', pack)

    def test_schema_rejects_diagnostic_generation(self):
        pack = copy.deepcopy(self.packs['pet']); pack['references']['inventory'][0]['diagnostic_only'] = True
        with self.assertRaises(jsonschema.ValidationError): self.validate('subject-pack', pack)

    def test_profile_minimum_coverage_three_classes(self):
        for name, view, framing, expected in [('human','front','close-up','canonical-front'),('pet','three-quarter-front','full-body','canonical-full-body'),('virtual-character','rear','full-body','canonical-rear')]:
            with self.subTest(subject=name):
                plan = r.plan_evidence(self.packs[name], {'view':view,'framing':framing})
                self.assertEqual([a['id'] for a in plan['canonical_evidence']], [expected])

    def test_evidence_order_is_independent_of_inventory_order(self):
        pack = self.packs['pet']; shot={'view':'front','framing':'close-up'}
        expected=r.plan_evidence(pack,shot)
        other=copy.deepcopy(pack); other['references']['inventory'].reverse()
        self.assertEqual(r.plan_evidence(other,shot),expected)

    def test_unavailable_canon_is_not_replaced_by_external_or_continuity(self):
        pack = copy.deepcopy(self.packs['pet']); pack['references']['inventory'] = []
        with self.assertRaises(r.Blocked) as caught: r.plan_evidence(pack, {'view':'front','framing':'close-up'})
        self.assertEqual(caught.exception.code,'CANONICAL_EVIDENCE_UNAVAILABLE')

    def test_explicit_required_anchor_is_not_optimized_away(self):
        pack=copy.deepcopy(self.packs['pet']); profile=pack['references']['profiles'][0]
        profile['require']['assets']=['canonical-full-body']
        plan=r.plan_evidence(pack,{'view':'front','framing':'close-up'})
        self.assertIn('canonical-full-body',[a['id'] for a in plan['canonical_evidence']])

    def test_unknown_profile_or_group_blocks(self):
        for shot in ({'view':'front','framing':'close-up','reference_profile':'missing'}, {'view':'front','framing':'close-up','required_invariant_groups':['imagined']}):
            with self.subTest(shot=shot), self.assertRaises(r.Blocked): r.plan_evidence(self.packs['pet'],shot)

    def test_anonymous_end_to_end_dry_runs(self):
        cases = [('human','front','close-up'),('pet','three-quarter-front','full-body'),('virtual-character','rear','full-body')]
        for name, view, framing in cases:
            with self.subTest(subject=name):
                pack=self.packs[name]; subject={'id':pack['subject']['id'],'pack_revision':r.digest(pack)}
                state=r.new_session(subject)
                handoff=r.prompt_handoff(subject,{'camera':view,'framing':framing},{'S1':{'view':view}}, {})
                self.assertFalse(handoff['canonical_transport_performed'])
                shot={'id':'S1','view':view,'framing':framing}
                plan=r.plan_evidence(pack,shot)
                p=base_packet();p.update(subject=subject,shot=shot,effective_spec=handoff['effective_spec'],canonical_evidence=plan['canonical_evidence'])
                p['postprocess_hooks']=copy.deepcopy(pack['postprocess']['hooks'])
                packet=r.freeze_packet(p);self.validate('generation-packet',packet.data)
                receipts={a['id']:{'handle':'sim:'+a['id'],'usable':True,'sha256':r.digest(a['id']),'simulation':True} for a in plan['canonical_evidence']}
                r.assert_materialized(packet,receipts,set(r.EXTERNAL),simulation=True)
                image=b'SYNTHETIC MODEL OUTPUT - NOT IMAGE ACCEPTANCE'
                for hook in p['postprocess_hooks']:
                    image=r.run_hook(hook['stage'],hook,image,{hook['id']:lambda b:b+b' finalized'})
                verdict=r.classify_result(reports(),VALIDATORS)
                c={'id':name+'-mock','kind':'CLEAN_MASTER_CANDIDATE','sha256':hashlib.sha256(image).hexdigest(),'packet_hash':packet.semantic_hash,'simulation':True}
                accepted=r.accept_master(packet,c,verdict,c['sha256'],True)
                state['accepted_clean_master']=accepted
                state['continuity_auxiliaries'].append(r.admit_continuity(accepted,subject))
                self.assertEqual(state['continuity_auxiliaries'][0]['classification'],'ACCEPT')
                derivative={**accepted,'kind':'DELIVERY_DERIVATIVE'}
                with self.assertRaises(r.Blocked):r.admit_continuity(derivative,subject)
                self.validate('runtime-state',state)


if __name__=='__main__': unittest.main()
