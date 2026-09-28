from generator import dossier


def test_reproducible(example_procedure):
    a = dossier.build(example_procedure, 42, 3)
    b = dossier.build(example_procedure, 42, 3)
    assert a == b
    assert dossier.build(example_procedure, 42, 4) != a


def test_shared_persona_across_documents(example_procedure):
    for i in range(50):
        d = dossier.build(example_procedure, 7, i)
        for doc in d["documents"]:
            f = doc["fields"]["so_cccd"]
            if f["mutated_by"] is None:
                assert f["value"] == d["persona"]["cccd"]


def test_labels_match_mutations(example_procedure):
    seen = set()
    for i in range(200):
        d = dossier.build(example_procedure, 1, i)
        label, reasons = d["decision"]["label"], d["decision"]["reasons"]
        if label == "approve":
            assert reasons == [] and d["missing_documents"] == []
            assert all(f["mutated_by"] is None for doc in d["documents"] for f in doc["fields"].values())
        else:
            assert len(reasons) == 1
            seen.add(reasons[0]["mutation"])
        if "M01" in {r["mutation"] for r in reasons}:
            assert d["missing_documents"] == ["giay-xac-nhan-example"]
        if "M04" in {r["mutation"] for r in reasons}:
            doc = next(x for x in d["documents"] if x["doc_type"] == "giay-xac-nhan-example")
            assert doc["fields"]["ngay_ky"]["value"] > d["submit_date"]
    assert seen == {"M01", "M02", "M03", "M04"}
