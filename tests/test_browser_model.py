"""Cross-language regression: browser policy must agree with the reference model."""
import itertools
import json
from pathlib import Path
import re
import subprocess
import unittest
from autonomy.evidence import route_assessment
from autonomy.policy import Request, decide

ROOT = Path(__file__).resolve().parents[1]

class BrowserModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.code = re.search(r'<script id="lab-code">(.*?)</script>', (ROOT/'index.html').read_text(), re.S).group(1)

    def js(self, expression):
        source = self.code + '\nprocess.stdout.write(JSON.stringify(' + expression + '));'
        return json.loads(subprocess.check_output(['node', '-e', source], text=True))

    def test_route_and_policy_parity(self):
        cases=[]
        expected=[]
        for advertised, required, exists in itertools.product((True,False),(True,False),(True,False,None)):
            for independent in ((True,False,None) if exists is True else (None,)):
                route=route_assessment(advertised=advertised,required=required,exists=exists,independent=independent)
                for authority,rights,evidence,paused in itertools.product((True,False,None),(True,False,None),(True,False,None),(True,False)):
                    cases.append(dict(advertised=advertised,required=required,exists=exists,independent=independent,authority=authority,rights=rights,evidence=evidence,paused=paused))
                    gate=decide(Request('read','public-synthetic-note','counterparty',authority,rights,evidence,required,route['route_control']=='PASS',paused))
                    expected.append([route['existence_claim_accuracy'],route['route_control'],gate['decision']])
        # Avoid shell/argv size limits: pass test data through standard input.
        source=self.code+'\nconst fs=require("fs");const cases=JSON.parse(fs.readFileSync(0,"utf8"));process.stdout.write(JSON.stringify(cases.map(s=>{const a=AutonomyLab.assess(s);return [a.claim,a.route,a.gate]})));'
        actual=json.loads(subprocess.check_output(['node','-e',source],input=json.dumps(cases),text=True))
        self.assertEqual(actual,expected)
        self.assertEqual(len(cases),1080)

    def test_exercise_boundaries(self):
        cases=[({},'PASS','ALLOW'),({'effect':False},'FAIL','DENY'),({'scope':False},'FAIL','DENY'),({'basis':False},'UNRESOLVED','DENY'),({'custody':False},'UNRESOLVED','DENY'),({'authority':False},'BLOCKED','DENY'),({'rights':False},'BLOCKED','DENY'),({'paused':True},'BLOCKED','DENY'),({'advertised':False,'required':False,'exists':False,'independent':None},'N/A','DENY')]
        actual=self.js(json.dumps([c[0] for c in cases])+'.map(s=>AutonomyLab.exercise({...AutonomyLab.defaults,...s}))')
        self.assertEqual([(r['verdict'],r['state']) for r in actual],[(c[1],c[2]) for c in cases])

    def test_no_live_assurance_upgrade(self):
        self.assertEqual(self.js('AutonomyLab.assess(AutonomyLab.defaults)')['live_assurance'],'UNRESOLVED')
