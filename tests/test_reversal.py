import copy
from pathlib import Path
import tempfile
import unittest

from autonomy.demo import build_case
from autonomy.evidence import STAGES, SIGNERS, digest, sign, verify, route_assessment


class ReversalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.bundle, self.registry, self.keys = build_case(self.tmp.name)

    def resign(self):
        refs = {"basis": {"mandate_hash":"mandate"}, "custody":{"basis_hash":"basis"},
                "decision":{"basis_hash":"basis","custody_hash":"custody"},
                "challenge":{"decision_hash":"decision"},
                "review":{"decision_hash":"decision","challenge_hash":"challenge"},
                "effect":{"review_hash":"review","mandate_hash":"mandate"},
                "observation":{"effect_hash":"effect"}}
        for stage in STAGES:
            p = self.bundle["records"][stage]["payload"]
            for field, target in refs.get(stage, {}).items():
                p[field] = digest(self.bundle["records"][target])
            self.bundle["records"][stage] = sign(SIGNERS[stage], p, self.keys[SIGNERS[stage]])

    def check_fail(self, text=None):
        result = verify(self.bundle, self.registry)
        self.assertEqual(result["technical_verdict"], "FAIL", result)
        if text: self.assertIn(text, result["reason"])

    def test_positive_correction_has_observable_effect(self):
        result = verify(self.bundle, self.registry)
        self.assertEqual(result["technical_verdict"], "PASS")
        self.assertEqual(result["live_reversal_assurance"], "UNRESOLVED")
        self.assertIn('"outcome": "ALLOW"', (Path(self.tmp.name)/"mock-resource-state.json").read_text())
        self.assertEqual(len(list((Path(self.tmp.name)/"records").glob('*/*.json'))), 8)

    def test_without_registry_unresolved(self):
        self.assertEqual(verify(self.bundle)["technical_verdict"], "UNRESOLVED")

    def test_every_missing_stage_is_unresolved(self):
        for stage in STAGES:
            b = copy.deepcopy(self.bundle); del b["records"][stage]
            with self.subTest(stage=stage):
                self.assertEqual(verify(b,self.registry)["technical_verdict"], "UNRESOLVED")

    def test_tampered_signed_basis_fails(self):
        self.bundle["records"]["basis"]["payload"]["rationale"] = "Changed after the fact"
        self.check_fail()

    def test_signed_payload_is_an_independent_snapshot(self):
        p = {"scope": {"resource": "before"}}
        envelope = sign("decider", p, self.keys["decider"])
        p["scope"]["resource"] = "after"
        self.assertEqual(envelope["payload"]["scope"]["resource"], "before")

    def test_decider_cannot_sign_review(self):
        p = self.bundle["records"]["review"]["payload"]
        self.bundle["records"]["review"] = sign("reviewer", p, self.keys["decider"])
        self.check_fail()

    def test_wrong_role_fails(self):
        self.bundle["records"]["review"]["role"] = "decider"
        self.check_fail("Wrong signer")

    def test_shared_keys_fail(self):
        self.registry["keys"]["reviewer"] = self.registry["keys"]["decider"]
        self.check_fail("share a signing key")

    def test_custody_after_decision_fails(self):
        self.bundle["records"]["custody"]["payload"]["tick"] = 4
        self.resign(); self.check_fail("precede act")

    def test_record_only_reversal_fails(self):
        self.bundle["records"]["effect"]["payload"]["after"] = "DENY"
        self.resign(); self.check_fail("observed state")

    def test_observer_must_see_correction(self):
        self.bundle["records"]["observation"]["payload"]["observed"] = "DENY"
        self.resign(); self.check_fail("observed state")

    def test_reviewer_cannot_expand_scope(self):
        self.bundle["records"]["effect"]["payload"]["scope"]["resource"] = "other-resource"
        self.resign(); self.check_fail("exceeds authorized scope")

    def test_expired_mandate_fails(self):
        self.bundle["records"]["mandate"]["payload"]["expires_tick"] = 6
        self.resign(); self.check_fail("expired")

    def test_revoked_consent_fails(self):
        self.bundle["records"]["effect"]["payload"]["consent_current"] = False
        self.resign(); self.check_fail("current consent")

    def test_rights_conflict_fails(self):
        self.bundle["records"]["effect"]["payload"]["rights_clear"] = False
        self.resign(); self.check_fail("rights clearance")

    def test_stale_permission_fails(self):
        self.bundle["records"]["effect"]["payload"]["authorization_version"] = 2
        self.resign(); self.check_fail("Stale authority")

    def test_same_outcome_is_not_reversal(self):
        self.bundle["records"]["review"]["payload"]["replacement"] = "DENY"
        self.resign(); self.check_fail("No changed decision")

    def test_case_replay_fails(self):
        self.bundle["case_id"] = "another-case"
        self.check_fail("Case")

    def test_wrong_state_hash_fails(self):
        self.bundle["records"]["observation"]["payload"]["state_sha256"] = "0"*64
        self.resign(); self.check_fail("digest")

    def test_whole_rewrite_fails_against_original_keys(self):
        with tempfile.TemporaryDirectory() as d:
            other, other_registry, _ = build_case(d)
        self.assertEqual(verify(other,self.registry)["technical_verdict"], "FAIL")
        self.assertEqual(verify(other,other_registry)["technical_verdict"], "PASS")
        self.assertEqual(verify(other,other_registry)["live_reversal_assurance"], "UNRESOLVED")

    def test_non_synthetic_claim_is_rejected(self):
        self.bundle["synthetic"] = False
        self.check_fail("synthetic")

    def test_malformed_bundle_fails(self):
        for b in [None, [], {}, {"policy":"wrong"}]:
            self.assertEqual(verify(b,self.registry)["technical_verdict"], "FAIL")

    def test_registries_do_not_persist_private_keys(self):
        for path in Path(self.tmp.name).rglob("*"):
            if path.is_file(): self.assertNotIn("PRIVATE KEY",path.read_text())


class RouteTests(unittest.TestCase):
    def test_claimed_route_absent(self):
        r=route_assessment(advertised=True,required=True,exists=False,independent=None)
        self.assertEqual((r['existence_claim_accuracy'],r['route_control']),('FAIL','FAIL'))

    def test_silence_does_not_excuse_required_control(self):
        r=route_assessment(advertised=False,required=True,exists=False,independent=None)
        self.assertEqual((r['existence_claim_accuracy'],r['route_control']),('N/A','FAIL'))

    def test_optional_unclaimed_route_is_not_pass(self):
        r=route_assessment(advertised=False,required=False,exists=False,independent=None)
        self.assertEqual(r['route_control'],'N/A')

    def test_unknown_is_not_absent(self):
        r=route_assessment(advertised=True,required=True,exists=None,independent=None)
        self.assertEqual((r['existence_claim_accuracy'],r['route_control']),('UNRESOLVED','UNRESOLVED'))

    def test_existing_but_dependent(self):
        r=route_assessment(advertised=True,required=True,exists=True,independent=False)
        self.assertEqual((r['existence_claim_accuracy'],r['route_control']),('PASS','FAIL'))

    def test_existing_independence_unknown(self):
        self.assertEqual(route_assessment(advertised=True,required=True,exists=True,independent=None)['route_control'],'UNRESOLVED')

    def test_verified_route_still_needs_remedy_test(self):
        r=route_assessment(advertised=True,required=True,exists=True,independent=True)
        self.assertEqual(r['route_control'],'PASS')
        self.assertIn('remedy still needs testing',r['reason'])

    def test_contradictory_inputs_rejected(self):
        with self.assertRaises(ValueError):route_assessment(advertised=True,required=True,exists=False,independent=True)
