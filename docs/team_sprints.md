# Team Roles and Sprint Timeline

## Team Members

* **Dhruv** (Team Leader) — Role: AI/ML and OCR Specialist
* **Unnati** (Team Member 1) — Role: Database Admin and DevOps
* **Utkarsh** (Team Member 2) — Role: Backend and API Developer
* **Yash** (Team Member 3) — Role: UI/UX and Frontend Specialist

---

## Form 1: Proposed Project Sprints

| S.No. | SPRINT NAME | PROPOSED USER STORY OF RESPECTIVE SPRINT |
| :--- | :--- | :--- |
| **1** | Core Backend & DB Setup | 1. Design Flask backend application architecture.<br>2. Build core backend service module for Devanagari syllable segmentation.<br>3. Design relational database schema and ingest 46+ Sanskrit meter definitions. |
| **2** | API & Caching Layer | 1. Develop RESTful API endpoints for verse analysis.<br>2. Develop optimized database indexing and in-memory caching layer. |
| **3** | Sandhi Backend & UI Setup | 1. Build backend service layer for Padaccheda and Sandhi splitting.<br>2. Set up React/Vite architecture and implement Tailwind UI input forms. |
| **4** | API State, UI & AI Translation | 1. Implement backend request validation.<br>2. Develop Axios API service layer.<br>3. Build visual React components for Laghu-Guru markers.<br>4. Integrate Gemini/Groq LLM APIs for translation services. |
| **5** | Dashboard & OCR Pipeline | 1. Build results dashboard grid layout.<br>2. Develop image preprocessing filters and Tesseract OCR engine integration. |
| **6** | OCR Autocorrection & User DB | 1. Develop OCR autocorrection module.<br>2. Prepare training datasets of Sanskrit verses.<br>3. Design SQL database models for user profiles and history. |
| **7** | LSTM Deep Learning & Auth | 1. Build and train PyTorch LSTM neural network.<br>2. Integrate trained LSTM model into backend.<br>3. Optimize React rendering.<br>4. Implement JWT authentication. |
| **8** | Testing, Docker & Cloud | 1. Conduct backend integration testing.<br>2. Perform frontend testing and deploy to Vercel.<br>3. Containerize Flask application using Docker.<br>4. Deploy production PostgreSQL database. |

---

## Form 2: Roles & Responsibilities Breakdown

### Dhruv (Role: AI/ML & OCR)
| START DATE | END DATE | DETAILS OF TASK COMPLETED UNDER THE USER STORY |
| :--- | :--- | :--- |
| 04/10/2026 | 31/10/2026 | Constructed AI service client to interface with LLM endpoints and engineer prompts for English and Hindi verse translations. |
| 01/11/2026 | 30/11/2026 | Implemented OpenCV image binarization filters and PyTesseract wrapper to extract Sanskrit text from uploaded image files. |
| 01/12/2026 | 15/12/2026 | Wrote heuristic post-processing algorithms that leverage meter patterns to fix optical character recognition misreadings. |
| 16/12/2026 | 02/01/2027 | Compiled corpus of Sanskrit verses and generated augmented, noisy training samples for deep learning model training. |
| 03/01/2027 | 20/01/2027 | Designed and trained bidirectional PyTorch LSTM model architecture to predict meter classes for irregular input verses. |
| 21/01/2027 | 06/02/2027 | Integrated trained PyTorch model inference engine into main backend service workflow to handle unclassified meters. |

### Unnati (Role: Database Admin & DevOps)
| START DATE | END DATE | DETAILS OF TASK COMPLETED UNDER THE USER STORY |
| :--- | :--- | :--- |
| 01/08/2026 | 22/08/2026 | Modeled relational database schema using SQLAlchemy and executed migration scripts to ingest 46 meter definitions. |
| 23/08/2026 | 15/09/2026 | Configured database table indices and built in-memory Redis caching service for high-speed meter pattern queries. |
| 01/12/2026 | 02/01/2027 | Designed SQL schema models for user authentication data, saved verse records, and historical analysis logs. |
| 03/01/2027 | 06/02/2027 | Implemented secure password hashing (bcrypt), JSON Web Token generation, and authorization header validation. |
| 07/02/2027 | 20/02/2027 | Created Dockerfiles and docker-compose configurations to package Flask API, database, and cache services into containers. |
| 21/02/2027 | 06/03/2027 | Provisioned cloud PostgreSQL database, configured production environment secrets, and deployed backend containers. |

### Utkarsh (Role: Backend & API Developer)
| START DATE | END DATE | DETAILS OF TASK COMPLETED UNDER THE USER STORY |
| :--- | :--- | :--- |
| 01/08/2026 | 12/08/2026 | Architected the modular Flask application structure, configured environment variables, and initialized backend app factory pattern. |
| 13/08/2026 | 22/08/2026 | Implemented backend Python services for Devanagari text processing, syllable extraction, and Laghu-Guru rule evaluation. |
| 23/08/2026 | 15/09/2026 | Created secure Flask REST API controllers to process verse payload requests and return structured JSON meter analysis responses. |
| 16/09/2026 | 03/10/2026 | Programmed backend service routines for decomposing compound Sanskrit words and exposing word breakdown API routes. |
| 04/10/2026 | 31/10/2026 | Built Flask request parsing middleware, input sanitization routines, and centralized error handling logic for invalid payloads. |
| 07/02/2027 | 06/03/2027 | Developed comprehensive automated integration test suite using pytest to validate API routes, services, and error handlers. |

### Yash (Role: UI/UX & Frontend Specialist)
| START DATE | END DATE | DETAILS OF TASK COMPLETED UNDER THE USER STORY |
| :--- | :--- | :--- |
| 16/09/2026 | 03/10/2026 | Initialized React repository with Vite, configured Tailwind CSS utility classes, and constructed main input form interfaces. |
| 04/10/2026 | 15/10/2026 | Built frontend HTTP service layer using Axios to handle async requests and manage application state across React views. |
| 16/10/2026 | 31/10/2026 | Developed custom interactive React components to display color-coded Laghu ('L') and Guru ('G') prosodic indicators. |
| 01/11/2026 | 30/11/2026 | Created responsive multi-card dashboard interface for presenting meter matching scores, verse breakdown, and translations. |
| 03/01/2027 | 06/02/2027 | Applied React memoization hooks, fixed layout shifts on mobile devices, and resolved cross-component rendering bugs. |
| 07/02/2027 | 06/03/2027 | Conducted end-to-end UI testing, configured production build optimization, and deployed web client to Vercel hosting. |
