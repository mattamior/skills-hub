"""Scope and approval regressions; all receipts remain synthetic test inputs."""
import unittest
from .test_runtime import r, base_packet, candidate, reports, VALIDATORS, SKILL
import yaml

class BoundaryEdges(unittest.TestCase):
    def test_additional_roles_remain_nonidentity(self):
        roles = ['TEXTURE', 'TEMPORARY_STYLING', 'EXPRESSION', 'GAZE']
        bound = r.resolve_image_roles([{'id': 'external'}], set(), explicit={'external': roles})
        plan = r.route_external(bound)
        self.assertEqual(plan[0]['roles'], sorted(roles))
        self.assertIn('NO_EXTERNAL_IDENTITY_TRANSFER', plan[0]['risk_guards'])
        p = base_packet(); p['external_evidence'] = plan; r.freeze_packet(p)

    def test_v1_can_short_circuit_later_layers(self):
        self.assertEqual(r.classify_result(reports('HARD_FAIL')[:1], VALIDATORS), 'HARD_RESET')

    def test_v2_can_short_circuit_local_quality(self):
        self.assertEqual(r.classify_result(reports(v2='OPERATION_FAIL')[:2], VALIDATORS), 'RETRY_REQUIRED')

    def test_real_dependency_blocker_still_precedes_short_circuit(self):
        self.assertEqual(r.classify_result(reports('HARD_FAIL')[:1], VALIDATORS, ['VALIDATOR_UNAVAILABLE']), 'BLOCKED')

    def test_single_profile_policy_is_not_implicit_union(self):
        pack = yaml.safe_load((SKILL/'references/fixtures/pet.yaml').read_text())
        pack['runtime'] = {'defaults': {'profile_selection': 'EXPLICIT_SINGLE'}}
        with self.assertRaises(r.Blocked): r.plan_evidence(pack, {'view':'front', 'framing':'close-up'})
        plan = r.plan_evidence(pack, {'view':'front', 'framing':'close-up', 'reference_profile':'face-closeup'})
        self.assertEqual(plan['matched_profiles'], ['face-closeup'])

    def test_required_conditional_asset_is_preserved(self):
        pack = yaml.safe_load((SKILL/'references/fixtures/pet.yaml').read_text())
        plan = r.plan_evidence(pack, {'view':'front','framing':'close-up','required_asset_ids':['canonical-full-body']})
        self.assertIn('canonical-full-body', [a['id'] for a in plan['canonical_evidence']])

    def post_gate_packet(self):
        p = base_packet(); p['route'] = 'CALIBRATION'; p['output_kind'] = 'CALIBRATION'
        p['gates'] = [{'id':'master-review', 'required':True, 'phase':'POST_VALIDATION', 'status':'OPEN'}]
        return r.freeze_packet(p)

    def test_pending_post_gate_allows_candidate_not_admission(self):
        packet = self.post_gate_packet(); c = candidate(packet)
        with self.assertRaises(r.Blocked) as caught: r.accept_master(packet,c,'ACCEPT',c['sha256'],True)
        self.assertEqual(caught.exception.code,'GATE_NOT_SATISFIED')

    def test_approval_for_other_candidate_is_not_reused(self):
        packet = self.post_gate_packet(); c = candidate(packet)
        approval = {'gate_id':'master-review','evidence_id':'approval-test','packet_hash':packet.semantic_hash,
                    'candidate_sha256':r.digest('other bytes'),'status':'PASSED'}
        with self.assertRaises(r.Blocked): r.accept_master(packet,c,'ACCEPT',c['sha256'],True,[approval])

    def test_post_gate_approval_is_hash_bound(self):
        packet = self.post_gate_packet(); c = candidate(packet)
        approval = {'gate_id':'master-review','evidence_id':'approval-test','packet_hash':packet.semantic_hash,
                    'candidate_sha256':c['sha256'],'status':'PASSED'}
        accepted = r.accept_master(packet,c,'ACCEPT',c['sha256'],True,[approval])
        self.assertEqual(accepted['kind'],'ACCEPTED_CLEAN_MASTER')
        self.assertEqual(packet.data['gates'][0]['status'],'OPEN')

    def test_unknown_gate_phase_blocks(self):
        p = base_packet(); p['gates']=[{'id':'x','phase':'LATER_SOMEHOW','required':True}]
        with self.assertRaises(r.Blocked): r.freeze_packet(p)

    def test_preview_route_cannot_mint_final(self):
        p = base_packet(); p['route']='PREVIEW_ONLY'
        with self.assertRaises(r.Blocked): r.freeze_packet(p)

    def test_external_authority_cannot_enter_canonical_channel(self):
        p = base_packet(); p['canonical_evidence'][0]['authority']='ROLE_SCOPED_EXTERNAL_REFERENCE'
        with self.assertRaises(r.Blocked): r.freeze_packet(p)

    def test_diagnostic_evidence_is_not_generation_input(self):
        p=base_packet(); p['canonical_evidence'][0]['diagnostic_only']=True
        with self.assertRaises(r.Blocked): r.freeze_packet(p)

    def test_simulated_item_blocks_even_with_live_looking_receipt(self):
        p=base_packet(); p['canonical_evidence'][0]['simulation']=True
        packet=r.freeze_packet(p)
        receipts={'canonical-front':{'usable':True,'handle':'opaque','sha256':r.digest('x')}}
        with self.assertRaises(r.Blocked): r.assert_materialized(packet,receipts,set(r.EXTERNAL))

    def test_invalid_checksum_is_not_transport_evidence(self):
        packet=r.freeze_packet(base_packet())
        receipts={'canonical-front':{'usable':True,'handle':'opaque','sha256':'not a checksum'}}
        with self.assertRaises(r.Blocked): r.assert_materialized(packet,receipts,set(r.EXTERNAL))

if __name__ == '__main__': unittest.main()
