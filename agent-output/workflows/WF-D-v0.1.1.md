---
id: WF-D-v0.1.1
title: Deployment v0.1.1
type: Deployment
parent: "[[WF-E1.2]]"
Planka-Card: "1729878166190688097"
artifact_hash: "8ee9228"
plan: "[[WF-P002]]"
version: v0.1.1
tag: 8ee9228
status: Released
date: 2026-03-16
artifacts:
  - "[Deployment Record](agent-output/deployment/v0.1.1.md)"
  - "[UAT Record](agent-output/uat/closed/002-UAT-persistent-memory.md)"
  - "[Implementation Record](agent-output/implementation/closed/002-persistent-memory-obsidian.md)"
---

# Deployment v0.1.1: Persistent Memory Pillar

## Summary
- Release `v0.1.1` deployed for the persistent-memory pillar.
- Epic 1.2 was validated through QA/UAT and transitioned to `Delivered`.
- Deployment finalized with commit/tag `8ee9228`.

The v0.1.1 release implements the primary security and structural requirements for the Persistent Memory Pillar.

## Key Changes
- **Memory Integrity**: Implementation of SHA-256 hashing for all `WF-*` nodes in `memory_utils.py` to prevent unauthorized modification.
- **Path Sanitization**: Root-relative path enforcement to prevent directory traversal in the vault.
- **Epic Gate**: Epic 1.2 is fully verified via automated QA and user UAT.

## Release Metadata
- **Commit**: 8ee9228
- **Tag**: `v0.1.1`
- **Confirmation**: Explicit user approval at 2026-03-13T12:05:00.

## Post-Execution
- Planka Epic card `1729878166190688097` moved to `Delivered`.
- All Stage 1 planning/QA/UAT documents moved to `closed/`.

## Artifacts
- [[agent-output/deployment/v0.1.1.md]]
- [[agent-output/uat/closed/002-UAT-persistent-memory.md]]
- [[agent-output/implementation/closed/002-persistent-memory-obsidian.md]]
