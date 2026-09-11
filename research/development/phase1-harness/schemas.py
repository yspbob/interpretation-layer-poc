"""Strict interchange records; schema validity never establishes truth."""
from jsonschema import Draft202012Validator


def obj(fields):
    return dict(type="object", properties=fields, required=list(fields), additionalProperties=False)


def array(items, maximum=64):
    return dict(type="array", items=items, maxItems=maximum)


def enum(*values):
    return dict(enum=list(values))


TEXT = dict(type="string", minLength=1, maxLength=12000)
ID = dict(type="string", pattern=r"^[A-Za-z0-9_]{1,48}$")
HASH = dict(type="string", pattern="^[a-f0-9]{64}$")
REF = obj(dict(path=TEXT, sha256=HASH, start=dict(type="integer", minimum=1),
               end=dict(type="integer", minimum=1), supports=TEXT))
CLAIM = obj(dict(id=ID, text=TEXT, kind=enum("observation", "recommendation", "constraint", "authority"),
                 scope=TEXT, exceptions=array(TEXT),
                 provenance=enum("documentation_extraction", "executable_text_restatement",
                                 "structural_inference", "unresolved"),
                 evidence=array(REF), counter_evidence=array(REF)))
DRAFT = obj(dict(claims=array(CLAIM, 32)))
DECISION = obj(dict(claim_id=ID, verdict=enum("admit", "reject", "unresolved"),
                    reason=TEXT, supported_scope=TEXT, evidence=array(REF),
                    contradictions=array(TEXT), missing_evidence=array(TEXT)))
REVIEW = obj(dict(decisions=array(DECISION, 32), action=enum("freeze", "revise", "stop_unresolved")))
GUIDANCE_ASSESSMENT = obj(dict(
    candidate_hash=HASH,
    claims=array(obj(dict(claim_id=ID, verdict=enum("supported", "unsupported", "unresolved"),
                          reason=TEXT)), 32),
    coverage=array(obj(dict(unit_id=ID, verdict=enum("covered", "missing", "unresolved"),
                            reason=TEXT)), 32)))
VERIFIER_ASSESSMENT = obj(dict(
    review_hash=HASH,
    decisions=array(obj(dict(claim_id=ID, expected=enum("admit", "reject", "unresolved"),
                             reason=TEXT)), 32)))


def validate(value, schema):
    Draft202012Validator(schema).validate(value)
