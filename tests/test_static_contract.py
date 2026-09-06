from pathlib import Path

SOURCE = Path("contracts/RetractionStatusGate.py").read_text(encoding="utf-8")

def test_runner_is_pinned():
    lines = SOURCE.splitlines()
    assert lines[0] == "# v0.2.16"
    assert lines[1] == '# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }'

def test_requester_only_submits_doi():
    signature = SOURCE.split("def request_status_check", 1)[1].split(") ->", 1)[0]
    assert "url" not in signature.lower()
    assert "digest" not in signature.lower()
    assert "doi: str" in signature

def test_validator_fetches_and_hashes_record():
    assert "gl.nondet.web.get(record_url)" in SOURCE
    assert "hashlib.sha256(response.body).hexdigest()" in SOURCE
    assert 'self.check_record_digests[check_id] = digest' in SOURCE
    assert "gl.eq_principle.strict_eq(evaluate)" in SOURCE

def test_identity_and_fail_closed_states_exist():
    assert "DOI_OR_PUBLISHER_IDENTITY_MISMATCH" in SOURCE
    assert 'verdict = "UNAVAILABLE"' in SOURCE
    assert '"IDENTITY_CONFLICT"' in SOURCE

def test_no_frontend_custody_or_submitted_digest():
    assert "emit_transfer" not in SOURCE
    assert "payable" not in SOURCE
    assert "frontend" not in SOURCE.lower()
    assert "submitted_digest" not in SOURCE

