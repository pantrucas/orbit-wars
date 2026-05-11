# SUBMISSION_LOG.md — Orbit Wars Kaggle Submission Log

Every Kaggle submission attempt must be recorded here before and after upload.
Do not delete entries. If an entry is wrong, append a correction note.

---

## Daily Submission Counter

| Date | Count used | Limit | Notes |
|---|---|---|---|
| 2026-05-10 | 0 | 5 | Project initialized |
| 2026-05-11 | 1 | 5 | Submission 001 — baseline-v0 |

---

## Submission Entries

---

### Submission 001 — baseline-v0 (ENVIADO 2026-05-11T01:28:12Z)

- Date/time: 2026-05-11T01:28:12Z
- Human approver: pantrucas ✓
- Assistant involved: Claude Code (Sonnet 4.6)
- Branch: main
- Commit hash: ce9eb4a
- Git diff clean?: Sí — repo subido a GitHub sin cambios pendientes
- Experiment ID: EXP001 (pendiente registro formal)
- File submitted: submission/main.py
- File SHA256: f97b929b425dc5c2f9f58b84880cf4655ba7358ad7dad7e767fa043457322240
- File size: 3125 bytes (3.05 KB)
- Kaggle command: `kaggle competitions submit orbit-wars -f submission/main.py -m "baseline-v0 greedy heuristic heartbeat"`
- Kaggle message: "baseline-v0 greedy heuristic heartbeat"
- Daily submission number: 1 de 5
- Validation result: PASS — entrypoint OK, sin imports prohibidos, sin red, sin secretos
- Local tournament result: 20/20 wins vs random (stub simulator — no mide ELO real)
- External data/models used: Ninguno — solo Python stdlib (math, random)
- Compliance status: Yellow-aceptado (ver detalle abajo)
- Kaggle status: ENVIADO ✓ — "Successfully submitted to Orbit Wars"
- Public score/rating: 600.0 — rank 1460/2475
- Error logs: —
- Observaciones: Primera submission heartbeat. Objetivo: confirmar que el formato es aceptado por Kaggle y que el agente no genera error runtime. No se espera score competitivo.
- Decision: Heartbeat confirmado. Agente funciona en producción sin errores runtime.
- Next action: Mejorar estrategia. Objetivo inmediato: superar rating 1000.

**Pipeline ejecutado (2026-05-10):**

| Check | Resultado |
|---|---|
| test_agent_contract (5 tests) | PASS |
| test_packaging (6 tests) | PASS |
| test_no_network (1 test) | PASS |
| test_reproducibility (2 tests) | PASS |
| validate_submission.py | PASS |
| package_submission.py --dry-run | PASS |
| check_submission_limit.py | PASS — 0/5 usadas |
| submit_kaggle.py --dry-run | PASS — comando generado, no ejecutado |

**Compliance gate:**

- [x] Sin items Red.
- [x] Cuenta Kaggle confirmada: pantrucas (COMPLIANCE.md Green).
- [x] Equipo confirmado: 1 miembro (COMPLIANCE.md Green).
- [x] Límite diario: 0/5 usadas.
- [x] Sin assets externos.
- [x] Sin red en código de agente.
- [x] Sin secretos en paquete.
- [x] Formato verificado: main.py, último def = agent(obs).
- [x] Commit hash registrado: ce9eb4a.
- [x] Aprobación humana explícita: pantrucas confirmó "CONFIRMO SUBIR A KAGGLE".

**Comando listo para ejecutar cuando pantrucas apruebe:**

```bash
python scripts/submit_kaggle.py \
  --file submission/main.py \
  --message "baseline-v0 greedy heuristic heartbeat" \
  --no-dry-run \
  --confirm "CONFIRMO SUBIR A KAGGLE"
```

---

### Template (copy for each submission)

```
### Submission <ID_OR_PENDING>

- Date/time:
- Human approver:
- Assistant involved:
- Branch:
- Commit hash:
- Git diff clean?:
- Experiment ID:
- File submitted:
- File SHA256:
- File size:
- Kaggle command:
- Kaggle message:
- Daily submission number:
- Validation result:
- Local tournament result:
- External data/models used:
- Compliance status:
- Kaggle status:
- Public score/rating:
- Error logs:
- Observations:
- Decision:
- Next action:

Checklist:
- [ ] Human explicitly approved submit.
- [ ] Daily limit checked (<5 today).
- [ ] Format verified (main.py or archive with main.py at top).
- [ ] Last def is agent function.
- [ ] Local validation passed.
- [ ] No secrets in package.
- [ ] No network/exfiltration code.
- [ ] Commit hash recorded.
- [ ] Compliance reviewed.
```
