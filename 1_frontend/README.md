# Member 1 — Frontend

## Role
Build and maintain the web UI for uploading PDF contracts and displaying extracted entities.

## Files
```
1_frontend/
├── index.html       # Main page
├── css/style.css    # Styling
├── js/app.js        # Upload logic, API calls, rendering
└── README.md
```

## How It Works
- Backend (`2_backend/app.py`) serves everything in this folder at `http://localhost:5000`
- `app.js` sends PDF to `POST /extract` and renders the JSON response
- No build step — edit files, refresh browser

## Test
```powershell
python 2_backend/app.py
# Open http://localhost:5000
```

---

## 30-Day Task Schedule

### Week 1 — Page Structure & Upload
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 1 | Mon | Create HTML skeleton with header, main area, footer | `index.html` |
| 2 | Tue | Build file upload form with browse button | `index.html` |
| 3 | Wed | Add drag-and-drop zone with visual feedback | `app.js` |
| 4 | Thu | Style upload section — dark theme, card layout | `style.css` |
| 5 | Fri | Add file validation (PDF only, max size 10MB) | `app.js` |

### Week 2 — API Integration & Results
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 6 | Mon | Connect upload to `POST /extract` using Fetch API | `app.js` |
| 7 | Tue | Add loading spinner and "Processing..." state | `app.js`, `style.css` |
| 8 | Wed | Create 4 result cards layout (Parties, Dates, Amounts, Clauses) | `index.html`, `style.css` |
| 9 | Thu | Render API response data into result cards | `app.js` |
| 10 | Fri | Add entity count badges on each card | `style.css`, `app.js` |

### Week 3 — Polish & UX
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 11 | Mon | Add "Show Raw JSON" toggle button | `app.js`, `style.css` |
| 12 | Tue | Error display — styled error card for failed uploads | `app.js`, `style.css` |
| 13 | Wed | Header health-check indicator (green dot when API online) | `app.js`, `style.css` |
| 14 | Thu | Fade-in animation for results, hover effects on cards | `style.css` |
| 15 | Fri | Responsive layout for mobile screens (media queries) | `style.css` |

### Week 4 — Accessibility & Cleanup
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 16 | Mon | Add ARIA labels and keyboard navigation | `index.html` |
| 17 | Tue | Focus states for buttons and interactive elements | `style.css` |
| 18 | Wed | Custom scrollbar styling for result lists | `style.css` |
| 19 | Thu | Cross-browser testing (Chrome, Firefox, Edge) | — |
| 20 | Fri | Fix any bugs found in cross-browser testing | `style.css` |

### Week 5 — Enhancement & Final
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 21 | Mon | Add file name display with remove button after selection | `app.js`, `style.css` |
| 22 | Tue | Add color-coded left borders on result cards per entity type | `style.css` |
| 23 | Wed | Add glassmorphism effect to upload card | `style.css` |
| 24 | Thu | Add subtle background gradient animation | `style.css` |
| 25 | Fri | Code cleanup — remove dead CSS, add comments | All files |

### Week 6 — Final Review
| Day | Date | Task | File(s) |
|-----|------|------|---------|
| 26 | Mon | Final visual review, pixel-perfect adjustments | `style.css` |
| 27 | Tue | Performance check — minify CSS if needed | `style.css` |
| 28 | Wed | Add meta tags for SEO (title, description, viewport) | `index.html` |
| 29 | Thu | Update this README with final notes | `README.md` |
| 30 | Fri | **Final submission** | All files |

---

## Commit Rules
- Commit only to `1_frontend/`
- Daily by 5 PM
- Format: `[frontend] Day X: description`
