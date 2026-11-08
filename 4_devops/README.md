# Member 4 — DevOps

## Role
Containerise the application with Docker, write test scripts, set up CI/CD, and maintain project-level documentation and configuration.

## Files
```
4_devops/
├── Dockerfile       # Container definition
└── README.md
```

## Also Responsible For (root level)
```
├── requirements.txt   # Aggregated dependencies
├── .gitignore         # Git ignore rules
└── README.md          # Root project documentation
```

## Docker Commands
```powershell
# 1. Build (Run Once)
docker build -t lexiscan -f 4_devops/Dockerfile .

# 2. First Run (Creates the container)
docker run -d -p 5000:5000 --name lexiscan lexiscan

# 3. Daily Usage (After it's created)
docker start lexiscan
docker stop lexiscan

# View logs
docker logs lexiscan

# Save image (for sharing)
docker save -o lexiscan.tar lexiscan
```

---

## 30-Day Task Schedule

### Week 1 — Dockerfile Foundation
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 1 | Mon | Write Dockerfile — base image `python:3.10-slim` | `Dockerfile` |
| 2 | Tue | Add system deps install (tesseract-ocr, poppler-utils) | `Dockerfile` |
| 3 | Wed | Add COPY, pip install, WORKDIR, EXPOSE steps | `Dockerfile` |
| 4 | Thu | Add NER training as build step (`RUN python 3_nlp_engine/train_ner.py`) | `Dockerfile` |
| 5 | Fri | Build and run container locally, verify `/health` returns ok | — |

### Week 2 — Testing & Requirements
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 6 | Mon | Aggregate all team deps into root `requirements.txt` | `../requirements.txt` |
| 7 | Tue | Create `.gitignore` (venv, __pycache__, models, temp files) | `../.gitignore` |
| 8 | Wed | Test PDF upload through Docker container | — |
| 9 | Thu | Fix any path issues inside container (relative vs absolute) | `Dockerfile` |
| 10 | Fri | Test all 3 sample PDFs through container API | — |

### Week 3 — Docker Optimization
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 11 | Mon | Optimize layer caching (install deps before COPY code) | `Dockerfile` |
| 12 | Tue | Add `.dockerignore` to reduce build context | `../.dockerignore` |
| 13 | Wed | Reduce image size — clean apt cache, use --no-cache-dir | `Dockerfile` |
| 14 | Thu | Test rebuild speed after optimizations | — |
| 15 | Fri | Document Docker commands in `4_devops/README.md` | `README.md` |

### Week 4 — CI/CD & Documentation
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 16 | Mon | Write root `README.md` with project overview | `../README.md` |
| 17 | Tue | Add Quick Start section (Docker + local) to root README | `../README.md` |
| 18 | Wed | Add team roles table and commit rules to root README | `../README.md` |
| 19 | Thu | Create `.github/workflows/ci.yml` for automated Docker build | `../.github/workflows/ci.yml` |
| 20 | Fri | Add health check test to CI pipeline | `../.github/workflows/ci.yml` |

### Week 5 — Integration Testing
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 21 | Mon | Write integration test script (Python — test all endpoints) | `test_integration.py` |
| 22 | Tue | Test `/health` and `/extract` with all 3 PDFs | `test_integration.py` |
| 23 | Wed | Test error paths (no file, wrong type, corrupt PDF) | `test_integration.py` |
| 24 | Thu | Run full regression through Docker | — |
| 25 | Fri | Document all test results | `README.md` |

### Week 6 — Final Delivery
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 26 | Mon | Full regression test — all endpoints, all PDFs, Docker + local | — |
| 27 | Tue | Create demo recording (screen record: upload PDF → see results) | — |
| 28 | Wed | Write SUBMISSION.md with Docker image name and demo link | `../SUBMISSION.md` |
| 29 | Thu | Push to Git repository, create release tag | — |
| 30 | Fri | **Final submission** | All files |

---

## Commit Rules
- Primary folder: `4_devops/`
- Also maintains: root `README.md`, `.gitignore`, `requirements.txt`
- Daily by 5 PM
- Format: `[devops] Day X: description`
