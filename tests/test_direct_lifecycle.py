import hashlib
import json

HOST = "raw.githubusercontent.com"
EVIDENCE_COMMIT = "910d9ac3efa766593b7f824996c10ff7f0ba551b"
PATH = "/Azaria723/RetractionStatusGate/" + EVIDENCE_COMMIT + "/evidence/"
ACTIVE = b'{"doi":"10.5555/active-001","publisher_key":"DEMO-PUBLISHER","title":"A reproducible active article","notice":"A correction fixed a table label. The article remains active and has not been retracted."}\n'
RETRACTED = b'{"doi":"10.5555/retracted-002","publisher_key":"DEMO-PUBLISHER","title":"A withdrawn result","notice":"This article was officially retracted by the publisher because its central dataset could not be validated."}\n'
CONCERN = b'{"doi":"10.5555/concern-003","publisher_key":"DEMO-PUBLISHER","title":"A result under review","notice":"The publisher issued an expression of concern while the underlying images are investigated. The article has not been retracted."}\n'

def deploy(direct_vm, direct_deploy, owner):
    direct_vm.strict_mocks = True
    direct_vm.check_pickling = True
    with direct_vm.prank(owner):
        return direct_deploy("contracts/RetractionStatusGate.py")

def register(direct_vm, contract, owner):
    with direct_vm.prank(owner):
        assert contract.register_publisher("DEMO-PUBLISHER", "10.5555", HOST, PATH) == 0

def request(direct_vm, contract, requester, doi):
    with direct_vm.prank(requester):
        assert contract.request_status_check(doi) == 0

def mock_record(direct_vm, suffix, body, status=200):
    direct_vm.mock_web(r"https://raw\.githubusercontent\.com/Azaria723/RetractionStatusGate/910d9ac3efa766593b7f824996c10ff7f0ba551b/evidence/" + suffix + r"\.json$", {"status": status, "body": body})

def result(contract):
    return json.loads(contract.get_check(0))

def run_case(direct_vm, direct_deploy, owner, requester, doi, body, verdict):
    contract = deploy(direct_vm, direct_deploy, owner)
    register(direct_vm, contract, owner)
    request(direct_vm, contract, requester, doi)
    mock_record(direct_vm, doi.split("/")[1], body)
    direct_vm.mock_llm(r"Classify the current.*", json.dumps({"verdict": verdict}))
    assert contract.assess_status(0) == verdict
    stored = result(contract)
    assert stored["verdict"] == verdict
    assert stored["record_sha256"] == hashlib.sha256(body).hexdigest()
    assert json.loads(stored["diagnostics"])["identity"] == "MATCH"

def test_correction_only_is_active(direct_vm, direct_deploy, direct_alice, direct_bob):
    run_case(direct_vm, direct_deploy, direct_alice, direct_bob, "10.5555/active-001", ACTIVE, "ACTIVE")

def test_official_retraction_is_retracted(direct_vm, direct_deploy, direct_alice, direct_bob):
    run_case(direct_vm, direct_deploy, direct_alice, direct_bob, "10.5555/retracted-002", RETRACTED, "RETRACTED")

def test_concern_without_retraction_is_concern(direct_vm, direct_deploy, direct_alice, direct_bob):
    run_case(direct_vm, direct_deploy, direct_alice, direct_bob, "10.5555/concern-003", CONCERN, "EXPRESSION_OF_CONCERN")

def test_validator_computes_live_digest_not_requester(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    register(direct_vm, contract, direct_alice)
    request(direct_vm, contract, direct_bob, "10.5555/active-001")
    changed = ACTIVE.replace(b"table label", b"figure label")
    mock_record(direct_vm, "active-001", changed)
    direct_vm.mock_llm(r"Classify the current.*", json.dumps({"verdict": "ACTIVE"}))
    assert contract.assess_status(0) == "ACTIVE"
    assert result(contract)["record_sha256"] == hashlib.sha256(changed).hexdigest()

def test_wrong_doi_identity_is_conflict_without_llm(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    register(direct_vm, contract, direct_alice)
    request(direct_vm, contract, direct_bob, "10.5555/active-001")
    wrong = ACTIVE.replace(b"10.5555/active-001", b"10.5555/other-999")
    mock_record(direct_vm, "active-001", wrong)
    assert contract.assess_status(0) == "IDENTITY_CONFLICT"
    assert result(contract)["reason_code"] == "DOI_OR_PUBLISHER_IDENTITY_MISMATCH"

def test_wrong_publisher_identity_is_conflict(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    register(direct_vm, contract, direct_alice)
    request(direct_vm, contract, direct_bob, "10.5555/active-001")
    wrong = ACTIVE.replace(b"DEMO-PUBLISHER", b"ATTACKER")
    mock_record(direct_vm, "active-001", wrong)
    assert contract.assess_status(0) == "IDENTITY_CONFLICT"

def test_source_failure_is_unavailable(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    register(direct_vm, contract, direct_alice)
    request(direct_vm, contract, direct_bob, "10.5555/active-001")
    mock_record(direct_vm, "active-001", ACTIVE, status=503)
    assert contract.assess_status(0) == "UNAVAILABLE"
    assert result(contract)["record_sha256"] == ""

def test_unknown_model_enum_fails_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    register(direct_vm, contract, direct_alice)
    request(direct_vm, contract, direct_bob, "10.5555/active-001")
    mock_record(direct_vm, "active-001", ACTIVE)
    direct_vm.mock_llm(r"Classify the current.*", json.dumps({"verdict": "TRUSTED"}))
    assert contract.assess_status(0) == "UNAVAILABLE"

def test_only_owner_registers_and_duplicates_fail(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    with direct_vm.prank(direct_bob):
        assert contract.register_publisher("DEMO-PUBLISHER", "10.5555", HOST, PATH) == "OWNER_ONLY"
    register(direct_vm, contract, direct_alice)
    with direct_vm.prank(direct_alice):
        assert contract.register_publisher("DEMO-PUBLISHER", "10.7777", HOST, PATH) == "PUBLISHER_KEY_ALREADY_REGISTERED"
        assert contract.register_publisher("OTHER", "10.5555", HOST, PATH) == "DOI_PREFIX_ALREADY_REGISTERED"
    assert json.loads(contract.get_counts())["publisher_count"] == 1

def test_doi_and_authority_injection_inputs_are_rejected(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    with direct_vm.prank(direct_alice):
        assert contract.register_publisher("DEMO", "10.5555", "localhost", PATH) == "INVALID_AUTHORITY_HOST"
        assert contract.register_publisher("DEMO", "10.5555", HOST, "/../secret/") == "INVALID_RECORD_PATH_PREFIX"
    register(direct_vm, contract, direct_alice)
    with direct_vm.prank(direct_bob):
        assert contract.request_status_check("https://doi.org/10.5555/active-001") == "INVALID_DOI"
        assert contract.request_status_check("10.5555/../../secret") == "INVALID_DOI"
        assert contract.request_status_check("10.9999/unknown") == "DOI_PREFIX_NOT_REGISTERED"
    assert json.loads(contract.get_counts())["check_count"] == 0

def test_deactivation_blocks_pending_check(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    register(direct_vm, contract, direct_alice)
    request(direct_vm, contract, direct_bob, "10.5555/active-001")
    with direct_vm.prank(direct_alice):
        assert contract.deactivate_publisher(0) == "PUBLISHER_DEACTIVATED"
    assert contract.assess_status(0) == "PUBLISHER_INACTIVE"
    assert result(contract)["status"] == 0

def test_repeat_request_creates_new_history_record(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    register(direct_vm, contract, direct_alice)
    with direct_vm.prank(direct_bob):
        assert contract.request_status_check("10.5555/active-001") == 0
        assert contract.request_status_check("10.5555/active-001") == 1
    assert json.loads(contract.get_counts())["check_count"] == 2
    assert json.loads(contract.get_check(0))["status"] == 0
    assert json.loads(contract.get_check(1))["status"] == 0
