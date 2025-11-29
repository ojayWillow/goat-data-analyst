# Corners Cut Log — 2025-11-28 (Day 4)

This document records pragmatic shortcuts taken during the project on this day, the reasons for doing so, and notes for future engineering work.

---

## 1. Datetime Type Detection in Profiling

**What:**  
Datetime detection in profiler.py currently uses a simple heuristic: 'Try to parse the first 100 non-null object values using pd.to_datetime(), suppress warnings, and if it works classify as datetime.'

**Why was this a shortcut?**  
The ideal method would use explicit format parsing and a ratio threshold, but we needed a safe, warning-free default to unblock progress.

**Plan for future revisit:**  
Replace with a robust helper, explicit format checks, and parsing thresholds.

---

## 2. Report Generator Structure

**What:**  
We use two files, base + wrapper, in export_engine.

**Why was this a shortcut?**  
Attempts to merge into one module failed on docstring/merge errors; two-file pattern is robust, but not perfect architecture.

**Plan for future revisit:**  
Merge only if real maintenance need appears.

---

## 3. Emoji & Encoding Handling

**What:**  
Stripped emojis and non-ASCII from headers and outputs.

**Why was this a shortcut?**  
Ensures predictable, warning-free behavior. True solution is reliable utf-8 everywhere and possible design updates.

**Plan for future revisit:**  
Reinstate only after stable layout/encoding pipeline.

---

## 4. Quality Report Layout

**What:**  
Left layout “good enough” pending further design needs.

---

**Reviewed & accepted by:**  
- [Your Name]
- 2025-11-28

---
