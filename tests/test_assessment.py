import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from services.assessment_engine import *

def test_questionnaire_has_40_plus_questions(): assert len(QUESTIONS)>=40

def test_private_answers_are_low():
    answers={q[0]:'no' for q in QUESTIONS}; r=assess(answers); assert r['score']==0; assert r['risk_level']=='LOW'

def test_public_exposure_increases_risk():
    answers={q[0]:'no' for q in QUESTIONS}; answers.update({'B1':'yes','C1':'yes','G1':'yes','E1':'yes'}); assert assess(answers)['score']>0

def test_boundaries():
    assert risk_level(20)=='LOW'; assert risk_level(21)=='MODERATE'; assert risk_level(40)=='MODERATE'; assert risk_level(41)=='HIGH'; assert risk_level(70)=='HIGH'; assert risk_level(71)=='CRITICAL'

def test_simulator_reduces_risk():
    answers={q[0]:'yes' for q in QUESTIONS}; x=simulate_improvement(answers,{'B1':'no','C1':'no','G1':'no','I3':'no'}); assert x['after']['score']<x['before']['score']

def test_findings_generated():
    answers={q[0]:'no' for q in QUESTIONS}; answers['B1']='yes'; answers['G1']='yes'; r=assess(answers); types={f['finding_type'] for f in r['findings']}; assert 'B1' in types and 'G1' in types
