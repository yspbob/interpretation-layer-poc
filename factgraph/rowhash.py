#!/usr/bin/env python3
"""Canonical row-dump hash of a fact-graph store (plan v1.2, section 5).

sha256(factgraph.db) depends on the SQLite build and page layout; this hash does
not. For every table, rows are dumped as JSON (sorted keys, sorted rows) and
hashed; the store hash is the hash of the per-table hashes. Two stores with the
same rows have the same rowhash whatever produced the file.

Usage: rowhash.py STORE.db [OTHER.db]   (with two stores, prints a per-table comparison)
"""
import sqlite3, hashlib, json, sys

def table_hashes(path):
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    out = {}
    for (t,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        cols = [c[1] for c in db.execute(f"PRAGMA table_info({t})")]
        rows = sorted(json.dumps(dict(zip(cols, r)), sort_keys=True, ensure_ascii=False)
                      for r in db.execute(f"SELECT * FROM {t}"))
        h = hashlib.sha256()
        for r in rows:
            h.update(r.encode("utf-8")); h.update(b"\n")
        out[t] = (h.hexdigest(), len(rows))
    return out

def store_hash(th):
    h = hashlib.sha256()
    for t in sorted(th):
        h.update(f"{t}:{th[t][0]}\n".encode())
    return h.hexdigest()

if __name__ == "__main__":
    a = table_hashes(sys.argv[1])
    print(f"store rowhash {store_hash(a)[:16]}  ({sys.argv[1]})")
    for t in sorted(a):
        print(f"  {t:12s} rows={a[t][1]:6d} {a[t][0][:16]}")
    if len(sys.argv) > 2:
        b = table_hashes(sys.argv[2])
        print(f"store rowhash {store_hash(b)[:16]}  ({sys.argv[2]})")
        for t in sorted(set(a) | set(b)):
            sa, sb = a.get(t), b.get(t)
            if sa is None: print(f"  {t:12s} only in second ({sb[1]} rows)")
            elif sb is None: print(f"  {t:12s} only in first ({sa[1]} rows)")
            elif sa[0] == sb[0]: print(f"  {t:12s} IDENTICAL ({sa[1]} rows)")
            else: print(f"  {t:12s} DIFFER ({sa[1]} vs {sb[1]} rows)")
