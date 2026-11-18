from dataclasses import replace
import unittest
from autonomy.policy import Request, decide


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.r=Request('share','synthetic-artifact','recipient-demo',True,True,True,True,True)

    def test_permitted_action_remains_possible(self):
        self.assertEqual(decide(self.r)['decision'],'ELIGIBLE')

    def test_withdrawn_packet_is_held(self):
        self.assertEqual(decide(replace(self.r,evidence_ready=False))['decision'],'HOLD')

    def test_revocation_is_denial(self):
        self.assertEqual(decide(replace(self.r,authority_current=False))['decision'],'DENY')

    def test_uncertainty_is_hold(self):
        self.assertEqual(decide(replace(self.r,authority_current=None))['decision'],'HOLD')

    def test_rights_are_a_hard_gate(self):
        self.assertEqual(decide(replace(self.r,rights_clear=False))['decision'],'DENY')

    def test_required_review_is_a_hard_gate(self):
        self.assertEqual(decide(replace(self.r,review_route_verified=False))['decision'],'HOLD')

    def test_operator_can_pause(self):
        self.assertEqual(decide(replace(self.r,operator_paused=True))['decision'],'HOLD')

    def test_no_blanket_refusal(self):
        self.assertEqual(decide(replace(self.r,review_required=False,review_route_verified=None))['decision'],'ELIGIBLE')

    def test_bad_findings_rejected(self):
        with self.assertRaises(ValueError):decide(replace(self.r,rights_clear='yes'))
