# Member 2 — Backend

## Role
Build and maintain the Flask REST API that serves the frontend, handles PDF uploads, runs the NLP pipeline, and returns structured JSON.

## Files
```
2_backend/
├── app.py         # Flask application
└── README.md
```

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Serves frontend UI from `1_frontend/` |
| GET | `/health` | Health check → `{"status": "ok"}` |
| POST | `/extract` | Accepts PDF → returns entities JSON |

## How It Works
- Imports `extract_text_from_pdf`, `extract_entities`, `postprocess` from `3_nlp_engine/`
- Serves `1_frontend/` as static files
- Saves uploaded PDF temporarily, runs pipeline, returns JSON, cleans up

## Test
```powershell
python 2_backend/app.py
curl http://localhost:5000/health
```

---

## 30-Day Task Schedule

### Week 1 — API Foundation
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 1 | Mon | Create Flask skeleton with `/health` GET endpoint | `app.py` |
| 2 | Tue | Add `/extract` POST endpoint stub (accept file, return mock JSON) | `app.py` |
| 3 | Wed | Add `sys.path` setup to import from `3_nlp_engine/` | `app.py` |
| 4 | Thu | Connect OCR: call `extract_text_from_pdf()` on uploaded file | `app.py` |
| 5 | Fri | Connect NER + postprocessor to complete the full pipeline | `app.py` |

### Week 2 — File Handling & Validation
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 6 | Mon | Validate file field exists in request (`multipart/form-data`) | `app.py` |
| 7 | Tue | Check file extension (PDF only), return 400 for invalid types | `app.py` |
| 8 | Wed | Implement temp file save and cleanup in `finally` block | `app.py` |
| 9 | Thu | Handle empty filename and missing file edge cases | `app.py` |
| 10 | Fri | Handle PDF with no extractable text (return empty arrays) | `app.py` |

### Week 3 — Frontend Serving & Logging
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 11 | Mon | Serve `1_frontend/` as static files from Flask | `app.py` |
| 12 | Tue | Serve `index.html` on GET `/` route | `app.py` |
| 13 | Wed | Add request logging with timestamps and file names | `app.py` |
| 14 | Thu | Log entity counts after each extraction | `app.py` |
| 15 | Fri | Add structured error JSON responses (400, 500) | `app.py` |

### Week 4 — Error Handling & Hardening
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 16 | Mon | Wrap pipeline in try/except — catch FileNotFoundError | `app.py` |
| 17 | Tue | Catch generic exceptions with 500 response | `app.py` |
| 18 | Wed | Add file size limit check (reject over 10MB) | `app.py` |
| 19 | Thu | Ensure temp_uploads directory auto-creates | `app.py` |
| 20 | Fri | Test all error paths manually (no file, wrong type, corrupt PDF) | — |

### Week 5 — Integration & Testing
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 21 | Mon | Test with `sample_pdfs/contract.pdf` — verify JSON output | — |
| 22 | Tue | Test with `lease_agreement.pdf` and `nda.pdf` | — |
| 23 | Wed | Fix any integration bugs found | `app.py` |
| 24 | Thu | Add response time logging (measure pipeline duration) | `app.py` |
| 25 | Fri | Code review — clean up imports, add docstrings | `app.py` |

### Week 6 — Final
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 26 | Mon | Run full end-to-end test with Docker container | — |
| 27 | Tue | Fix any Docker-related path issues | `app.py` |
| 28 | Wed | Add CORS headers if needed for cross-origin requests | `app.py` |
| 29 | Thu | Update this README with final API documentation | `README.md` |
| 30 | Fri | **Final submission** | All files |

---

## Commit Rules
- Commit only to `2_backend/`
- Daily by 5 PM
- Format: `[backend] Day X: description`
