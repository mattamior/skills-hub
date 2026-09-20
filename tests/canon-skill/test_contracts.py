"""Executable declaration regression, never a real-image acceptance claim."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import unittest

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'skills/canon-skill'
spec = importlib.util.spec_from_file_location('contracts', SKILL / 'scripts/contracts.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def load_pack(name='human'):
    return yaml.safe_load((SKILL / f'references/fixtures/{name}.yaml').read_text())


def packet(name='human', view='front', framing='close-up'):
    p = load_pack(name)
    plan = c.select_evidence(p, {'view':view, 'framing':framing}, [])
    return dict(schema_version='1.0', subject={'id':p['subject']['id'],'pack_revision':'fixture-1'},
        route='STANDALONE_SHOT', operation='GENERATE', output_kind='FINAL',
        effective_spec={'camera':view,'framing':framing},series_lock={'id':'series-1'},
        shot={'id':'shot-1','revision':'r1','view':view,'framing':framing},
        written_authority=p['canon']['written_authority'],canonical_evidence=plan['canonical_evidence'],external_evidence=[],continuity_evidence=[],
        image_roles={r['id']:'PROTECTED_CANONICAL' for r in plan['canonical_evidence']},
        edit_target=None,preview_reference=None,preserve_constraints=['canonical-invariants'],
        risk_guards=['NO_EXTERNAL_IDENTITY_TRANSFER'],preprocess_hooks=[],postprocess_hooks=p['postprocess']['hooks'],
        validators=[dict(id=x,layer=x,scope=['required'],revision='1') for x in ('V1','V2','V3')],
        required_gates=[],retry_policy={'automatic_hard_reset_limit':1,'eligible':True},delivery_policy={'id':'default-final'})


def report(p):
    return dict(packet_digest=c.digest(p),candidate_sha256='a'*64,dependencies='SATISFIED',phase='FINAL_VALIDATION',
        checks=[dict(id=v['id'],layer=v['layer'],outcome='PASS') for v in p['validators']],
        hooks={h['id']:'PASS' for h in p['preprocess_hooks']+p['postprocess_hooks']})


def master():
    return dict(id='master-1',subject_id='subject-1',subject_pack_revision='p1',series_id='series-1',
        shot_id='s1',shot_revision='r1',packet_digest='b'*64,candidate_sha256='a'*64,validated_sha256='a'*64,
        result_id='result-1',classification='ACCEPT',provenance='ACCEPTED_CLEAN_MASTER',output_kind='FINAL',
        validation_complete=True,provenance_verified=True,simulation=False,admitted_roles=['ENVIRONMENT'])


class Contracts(unittest.TestCase):
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(c.ContractError):c.load_json('{"id":"first","id":"last"}')

    def test_poisoned_extension_role_rejected(self):
        with self.assertRaises(c.ContractError):c.external_roles(['extension:style'],[],{'extension:style':{'allowed_influence':['primary_subject.identity']}})

    def test_all_bundled_schemas_are_valid(self):
        for path in (SKILL/'schemas').glob('*.json'):
            with self.subTest(schema=path.name):Draft202012Validator.check_schema(json.loads(path.read_text()))

    def test_three_subject_classes_same_contract(self):
        for name in ('human','pet','virtual-character'):
            with self.subTest(subject=name):c.validate_pack(load_pack(name))

    def test_subject_type_is_not_anatomy_switch(self):
        p=load_pack();p['subject']['type']='fixed-product';c.validate_pack(p)

    def test_no_human_required_key(self):
        p=load_pack('virtual-character');p['canon']['face']='unexpected'
        with self.assertRaises(c.ContractError):c.validate_pack(p)

    def test_optional_capabilities_absent(self):
        p=load_pack('pet');self.assertFalse(p['calibration']['enabled']);self.assertEqual(p['postprocess']['hooks'],[]);c.validate_pack(p)

    def test_duplicate_reference_rejected(self):
        p=load_pack();p['references']['inventory'].append(copy.deepcopy(p['references']['inventory'][0]))
        with self.assertRaises(c.ContractError):c.validate_pack(p)

    def test_dangling_profile_asset_rejected(self):
        p=load_pack();p['references']['profiles'][0]['prefer_assets']=['missing']
        with self.assertRaises(c.ContractError):c.validate_pack(p)

    def test_dangling_coverage_rejected(self):
        p=load_pack();p['references']['inventory'][0]['covers']=['missing']
        with self.assertRaises(c.ContractError):c.validate_pack(p)

    def test_unapproved_calibration_rejected(self):
        p=load_pack();p['references']['inventory'][0]['authority']='APPROVED_CALIBRATION'
        with self.assertRaises(c.ContractError):c.validate_pack(p)

    def test_diagnostic_cannot_be_generation_eligible(self):
        p=load_pack();p['references']['inventory'][0]['diagnostic_only']=True
        with self.assertRaises(c.ContractError):c.validate_pack(p)

    def test_disabled_calibration_has_no_profiles(self):
        p=load_pack('virtual-character');p['calibration']['enabled']=False
        with self.assertRaises(c.ContractError):c.validate_pack(p)

    def test_six_routes(self):
        state={'selected_shot':'s','shot_registry':{'s':{}}}
        for task,route in [({'calibration':True},'CALIBRATION'),({'shot_id':'s'},'EXISTING_SERIES_SHOT'),({'current_operation':'RETRY'},'CURRENT_SHOT_OPERATION'),({'preview':True},'PREVIEW_ONLY'),({'series':True},'SERIES'),({},'STANDALONE_SHOT')]:
            with self.subTest(route=route):self.assertEqual(c.resolve_route(task,state),route)

    def test_unknown_shot_not_created(self):
        with self.assertRaises(c.ContractError):c.resolve_route({'shot_id':'missing'},c.new_state())

    def test_retry_does_not_guess_from_history(self):
        with self.assertRaises(c.ContractError):c.resolve_route({'current_operation':'RETRY'},c.new_state())

    def test_stale_selected_shot_rejected(self):
        with self.assertRaises(c.ContractError):c.resolve_route({'current_operation':'RETRY'},{'selected_shot':'s'})

    def test_protected_beats_explicit_external(self):
        self.assertEqual(c.resolve_image_role(['EXPLICIT_EXTERNAL_ROLE','PROTECTED_CANONICAL']),'PROTECTED_CANONICAL')

    def test_edit_beats_reference(self):
        self.assertEqual(c.resolve_image_role(['EDIT_TARGET','EXPLICIT_EXTERNAL_ROLE']),'EDIT_TARGET')

    def test_preview_beats_continuity(self):
        self.assertEqual(c.resolve_image_role(['PREVIEW_SHOT_REFERENCE','ACCEPTED_CONTINUITY']),'PREVIEW_SHOT_REFERENCE')

    def test_edit_preview_retains_edit(self):
        self.assertEqual(c.resolve_image_role(['PREVIEW_SHOT_REFERENCE','EDIT_TARGET']),'EDIT_TARGET')

    def test_explicit_beats_fallback(self):
        self.assertEqual(c.external_roles(['LIGHTING'],['POSE','CAMERA']),['LIGHTING'])

    def test_no_implicit_primary_identity_role(self):
        with self.assertRaises(c.ContractError):c.external_roles(['IDENTITY'],[])

    def test_unscoped_original_is_not_automatic_full_authority(self):
        for roles in ([],['ORIGINAL_PROMPT_REFERENCE']):
            with self.subTest(roles=roles),self.assertRaises(c.ContractError):c.external_roles(None,roles)

    def test_subject_owned_external_extension(self):
        defs={'extension:surface-treatment':{'allowed_influence':['temporary.surface']}}
        self.assertEqual(c.external_roles(['extension:surface-treatment'],[],defs),['extension:surface-treatment'])
        with self.assertRaises(c.ContractError):c.external_roles(['extension:surface-treatment'],[])

    def test_original_nonhuman_role_retained(self):
        self.assertEqual(c.external_roles(['NON_HUMAN_SUBJECT'],[]),['NON_HUMAN_SUBJECT'])

    def test_front_minimal_subset(self):
        got=c.select_evidence(load_pack(),{'view':'front','framing':'close-up'},[])
        self.assertEqual([r['id'] for r in got['canonical_evidence']],['canonical-front'])

    def test_pet_full_body_coverage(self):
        got=c.select_evidence(load_pack('pet'),{'view':'three-quarter-front','framing':'full-body'},[])
        self.assertEqual([r['id'] for r in got['canonical_evidence']],['canonical-full-body'])
        self.assertIn('tail-structure',got['required_invariant_groups'])

    def test_virtual_rear_not_front_symbol(self):
        got=c.select_evidence(load_pack('virtual-character'),{'view':'rear','framing':'full-body'},[])
        self.assertEqual([r['id'] for r in got['canonical_evidence']],['canonical-rear'])
        self.assertNotIn('chest-symbol',got['required_invariant_groups'])

    def test_missing_canon_not_replaced(self):
        p=load_pack();p['references']['inventory']=[];p['references']['profiles'][0]['prefer_assets']=[];p['references']['profiles'][1]['prefer_assets']=[]
        with self.assertRaises(c.ContractError):c.select_evidence(p,{'view':'front','framing':'close-up'},[])

    def test_exact_required_profile_assets_preserved(self):
        p=load_pack();p['references']['profiles'][0]['require']['assets']=['canonical-front','canonical-full-body']
        got=c.select_evidence(p,{'view':'front','framing':'close-up'},[])
        self.assertEqual(len(got['canonical_evidence']),2)

    def test_mandatory_reference_order_is_preserved(self):
        p=load_pack();p['references']['profiles'][0]['require']['assets']=['canonical-full-body','canonical-front']
        got=c.select_evidence(p,{'view':'front','framing':'close-up'},[])
        self.assertEqual([r['id'] for r in got['canonical_evidence']],['canonical-full-body','canonical-front'])

    def test_primary_plus_conditional_supplement(self):
        p=load_pack();p['references']['profiles'][0]['require']['assets']=['canonical-front'];extra=copy.deepcopy(p['references']['profiles'][0]);extra.update(id='conditional',kind='SUPPLEMENT');extra['require']['assets']=['canonical-full-body'];p['references']['profiles'].append(extra)
        got=c.select_evidence(p,{'view':'front','framing':'close-up'},[])
        self.assertEqual(len(got['canonical_evidence']),2)

    def test_single_primary_profile_ambiguity_blocks(self):
        p=load_pack();other=copy.deepcopy(p['references']['profiles'][0]);other['id']='another';p['references']['profiles'].append(other)
        with self.assertRaises(c.ContractError):c.select_evidence(p,{'view':'front','framing':'close-up'},[])
        c.select_evidence(p,{'view':'front','framing':'close-up','reference_profile':'another'},[])

    def test_selection_stable_under_inventory_reordering(self):
        p=load_pack();a=c.select_evidence(p,{'view':'front','framing':'close-up'},[]);p['references']['inventory'].reverse()
        self.assertEqual(a,c.select_evidence(p,{'view':'front','framing':'close-up'},[]))

    def test_freeze_is_defensive_copy(self):
        p=packet();f=c.freeze(p);p['effective_spec']['camera']='rear';self.assertEqual(f['payload']['effective_spec']['camera'],'front')

    def test_frozen_mutation_rejected(self):
        f=c.freeze(packet());f['payload']['effective_spec']['camera']='rear'
        with self.assertRaises(c.ContractError):c.verify_frozen(f)

    def test_retry_keeps_packet_semantics(self):
        f=c.freeze(packet());self.assertEqual(c.retry(f,{'seed':42})['packet'],f)

    def test_retry_rejects_hidden_prompt_redesign(self):
        with self.assertRaises(c.ContractError):c.retry(c.freeze(packet()),{'prompt':'different'})

    def test_revision_only_authorized_paths(self):
        f=c.freeze(packet());changes={'/effective_spec/camera':'rear','/shot/revision':'r2'}
        with self.assertRaises(c.ContractError):c.revise(f,changes,['/shot/revision'])
        self.assertNotEqual(c.revise(f,changes,list(changes))['digest'],f['digest'])

    def test_revision_requires_new_identifier(self):
        with self.assertRaises(c.ContractError):c.revise(c.freeze(packet()),{'/effective_spec/camera':'rear'},['/effective_spec/camera'])

    def test_nonfinite_hash_rejected(self):
        for x in (math.nan,math.inf,-math.inf):
            with self.subTest(x=x),self.assertRaises(c.ContractError):c.digest({'x':x})

    def test_object_order_not_semantic(self):self.assertEqual(c.digest({'x':1,'y':2}),c.digest({'y':2,'x':1}))
    def test_array_order_is_semantic(self):self.assertNotEqual(c.digest(['x','y']),c.digest(['y','x']))

    def test_gate_not_satisfied_blocks_freeze(self):
        p=packet();p['required_gates']=[{'id':'identity','status':'OPEN'}]
        with self.assertRaisesRegex(c.ContractError,'GATE_NOT_SATISFIED'):c.freeze(p)

    def test_missing_hook_handler_blocks(self):
        p=packet();del p['postprocess_hooks'][0]['handler']
        with self.assertRaises(c.ContractError):c.freeze(p)

    def test_postvalidation_cannot_mutate_pixels(self):
        p=packet();p['postprocess_hooks'][0]['stage']='POST_VALIDATION'
        with self.assertRaises(c.ContractError):c.freeze(p)

    def test_all_five_results(self):
        p=packet()
        for layer,outcome,reason,expected in [('V1','HARD_FAIL','WRONG_SUBJECT_IDENTITY','HARD_RESET'),('V2','OPERATION_FAIL','CAMERA_NONCOMPLIANCE','RETRY_REQUIRED'),('V3','LOCAL_DEFECT','EDGE_DEFECT','REFINE_ELIGIBLE'),('V1','PASS',None,'ACCEPT'),('V1','BLOCKED',None,'BLOCKED')]:
            r=report(p);row=next(x for x in r['checks'] if x['layer']==layer);row.update(outcome=outcome,reason=reason)
            with self.subTest(expected=expected):self.assertEqual(c.classify(p,r,'a'*64),expected)

    def test_mixed_failure_precedence(self):
        p=packet();r=report(p);r['checks'][0].update(outcome='HARD_FAIL',reason='EXTERNAL_IDENTITY_CONTAMINATION');r['checks'][1].update(outcome='OPERATION_FAIL',reason='POSE_NONCOMPLIANCE')
        self.assertEqual(c.classify(p,r,'a'*64),'HARD_RESET')
        r['dependencies']='MISSING';self.assertEqual(c.classify(p,r,'a'*64),'BLOCKED')

    def test_small_canonical_detail_never_accepts_missing(self):
        p=packet();r=report(p);r['checks'][0].update(outcome='LOCAL_DEFECT',reason='SMALL_CANONICAL_DETAIL_DEFECT')
        self.assertEqual(c.classify(p,r,'a'*64),'REFINE_ELIGIBLE')

    def test_invalid_hard_reason_fails_closed(self):
        p=packet();r=report(p);r['checks'][0].update(outcome='HARD_FAIL',reason='NOT_PRETTY')
        self.assertEqual(c.classify(p,r,'a'*64),'BLOCKED')

    def test_missing_validator_cannot_look_correct(self):
        p=packet();r=report(p);r['checks'].pop();self.assertEqual(c.classify(p,r,'a'*64),'BLOCKED')

    def test_required_hook_failure_blocks(self):
        p=packet();r=report(p);r['hooks']={};self.assertEqual(c.classify(p,r,'a'*64),'BLOCKED')

    def test_candidate_hash_changed_after_validation(self):
        p=packet();self.assertEqual(c.classify(p,report(p),'b'*64),'BLOCKED')

    def test_report_from_other_packet_blocks(self):
        p=packet();r=report(p);p['effective_spec']['camera']='rear';self.assertEqual(c.classify(p,r,'a'*64),'BLOCKED')

    def test_construction_validation_not_final_acceptance(self):
        p=packet();r=report(p);r['phase']='CONSTRUCTION';self.assertEqual(c.classify(p,r,'a'*64),'BLOCKED')

    def test_one_safe_retry_and_all_second_results_stop(self):
        policy={'automatic_hard_reset_limit':1,'eligible':True}
        self.assertEqual(c.recovery_action('HARD_RESET',0,policy),'FRESH_RETRY_ONCE')
        for result in ('HARD_RESET','ACCEPT','BLOCKED','REFINE_ELIGIBLE','RETRY_REQUIRED'):
            with self.subTest(result=result):self.assertEqual(c.recovery_action(result,1,policy),'NONE')

    def test_retry_required_never_auto(self):self.assertEqual(c.recovery_action('RETRY_REQUIRED',0,{'automatic_hard_reset_limit':1,'eligible':True}),'NONE')
    def test_calibration_can_disable_retry(self):self.assertEqual(c.recovery_action('HARD_RESET',0,{'automatic_hard_reset_limit':0,'eligible':False}),'NONE')

    def test_invalid_retry_budget_rejected(self):
        with self.assertRaises(c.ContractError):c.recovery_action('HARD_RESET',2,{'automatic_hard_reset_limit':1,'eligible':True})

    def test_continuity_admission_positive_declaration(self):self.assertTrue(c.admit_continuity(master(),'subject-1','series-1'))

    def test_continuity_rejects_all_forbidden_provenance(self):
        for provenance in ('PREVIEW_ONLY','GENERATED_UNVERIFIED','CONSTRUCTION_INTERMEDIATE','DELIVERY_DERIVATIVE','CLEAN_MASTER_CANDIDATE'):
            m=master();m['provenance']=provenance
            with self.subTest(provenance=provenance):self.assertFalse(c.admit_continuity(m,'subject-1','series-1'))

    def test_continuity_rejects_nonaccept_results(self):
        for result in ('HARD_RESET','RETRY_REQUIRED','REFINE_ELIGIBLE','BLOCKED'):
            m=master();m['classification']=result
            with self.subTest(result=result):self.assertFalse(c.admit_continuity(m,'subject-1','series-1'))

    def test_simulated_acceptance_never_live_continuity(self):
        m=master();m['simulation']=True;self.assertFalse(c.admit_continuity(m,'subject-1','series-1'))

    def test_accepted_preview_never_clean_master(self):
        m=master();m['output_kind']='PREVIEW';self.assertFalse(c.admit_continuity(m,'subject-1','series-1'))

    def test_master_hash_mismatch_rejected(self):
        m=master();m['validated_sha256']='b'*64;self.assertFalse(c.admit_continuity(m,'subject-1','series-1'))

    def test_cross_subject_and_series_rejected(self):
        self.assertFalse(c.admit_continuity(master(),'other','series-1'));self.assertFalse(c.admit_continuity(master(),'subject-1','other'))

    def test_session_starts_empty_independently(self):
        a=c.new_state();a['shot_registry']['s']={};a['identity_gate']['status']='PASSED';b=c.new_state()
        self.assertEqual(b['shot_registry'],{});self.assertEqual(b['identity_gate']['status'],'OPEN');self.assertIsNone(b['generation_packet'])

    def test_named_preview_not_upscale_final(self):
        p=packet();p['preview_reference']={'id':'preview','asset':'fixture://preview','shot_id':'shot-1','sha256':'c'*64};p['image_roles']['preview']='PREVIEW_SHOT_REFERENCE'
        c.freeze(p);self.assertEqual(p['operation'],'GENERATE');self.assertIsNone(p['edit_target'])

    def test_edit_requires_real_target_declaration(self):
        p=packet();p['operation']='EDIT'
        with self.assertRaises(c.ContractError):c.freeze(p)

    def test_canonical_binding_cannot_be_pose(self):
        p=packet();p['image_roles']['canonical-front']='EXPLICIT_EXTERNAL_ROLE'
        with self.assertRaises(c.ContractError):c.freeze(p)

    def test_transport_receipts_exact_packet(self):
        f=c.freeze(packet());receipts=[dict(id=e['id'],sha256=e['sha256'],packet_digest=f['digest'],materialized=True,attached=True,handle='TEST-ONLY') for e in f['payload']['canonical_evidence']]
        c.verify_transport(f,receipts);receipts[0]['attached']=False
        with self.assertRaises(c.ContractError):c.verify_transport(f,receipts)

    def test_filename_only_not_transport(self):
        with self.assertRaises(c.ContractError):c.verify_transport(c.freeze(packet()),[])

    def test_unapproved_transport_bytes_rejected(self):
        f=c.freeze(packet());r=[dict(id=e['id'],sha256='0'*64,packet_digest=f['digest'],materialized=True,attached=True,handle='TEST-ONLY') for e in f['payload']['canonical_evidence']]
        with self.assertRaises(c.ContractError):c.verify_transport(f,r)

    def test_anonymous_end_to_end_dry_runs(self):
        for name,view,framing in [('human','front','close-up'),('pet','three-quarter-front','full-body'),('virtual-character','rear','full-body')]:
            with self.subTest(subject=name):
                state=c.new_state();p=packet(name,view,framing);f=c.freeze(p)
                self.assertEqual(c.classify(p,report(p),'a'*64),'ACCEPT')
                self.assertEqual(c.retry(f,{'seed':7})['packet']['digest'],f['digest'])
                self.assertIsNone(state['accepted_clean_master'])
                # Deliberately no simulated master is admitted into actual continuity.


if __name__=='__main__':unittest.main(verbosity=2)
