import json
import urllib.request

def main():
    base = "http://127.0.0.1:5000/api"
    
    # 1. Health
    h = json.loads(urllib.request.urlopen(f"{base}/health").read())
    assert h["status"] == "ok"
    print("[PASS] /api/health OK")
    
    # 2. Categories
    cats = json.loads(urllib.request.urlopen(f"{base}/categories").read())["categories"]
    assert len(cats) >= 8
    print(f"[PASS] /api/categories OK ({len(cats)} categories)")
    
    # 3. Symptoms for CAT_BRAKES
    syms = json.loads(urllib.request.urlopen(f"{base}/symptoms?category=CAT_BRAKES").read())["symptoms"]
    assert len(syms) > 0
    print(f"[PASS] /api/symptoms OK ({len(syms)} brake symptoms)")
    
    # 4. Follow-up questions
    req = urllib.request.Request(
        f"{base}/follow-up-questions",
        data=json.dumps({"category_id": "CAT_BRAKES", "symptom_ids": ["SYM_SOFT_OR_SPONGY_BRAKE_PEDAL"]}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    fq = json.loads(urllib.request.urlopen(req).read())
    print(f"[PASS] /api/follow-up-questions OK ({len(fq.get('questions', []))} questions)")
    
    # 5. Diagnose
    req = urllib.request.Request(
        f"{base}/diagnose",
        data=json.dumps({"category_id": "CAT_BRAKES", "symptom_ids": ["SYM_SOFT_OR_SPONGY_BRAKE_PEDAL"], "follow_up_answers": {}}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    diag = json.loads(urllib.request.urlopen(req).read())
    assert diag["status"] == "matched"
    assert len(diag["matches"]) > 0
    m = diag["matches"][0]
    assert "CLO" not in m.get("explanation", "")
    assert "RULE_" not in m.get("explanation", "")
    print(f"[PASS] /api/diagnose OK (Clean explanation: '{m.get('explanation')[:65]}...')")
    print(f"[PASS] Target Component: {m.get('affected_component')}")
    print(f"[PASS] Diagnosis Status: {m.get('diagnosis_status')}")

if __name__ == "__main__":
    main()
