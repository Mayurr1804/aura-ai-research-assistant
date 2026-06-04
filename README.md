# AURA AI Research Assistant 🚀

AURA is an autonomous AI-powered research copilot that helps researchers move from a research idea to a complete research workflow. 

Instead of manually searching papers, reading dozens of PDFs, finding datasets, identifying research gaps, and creating roadmaps, AURA automates the entire process.

## 🌟 Features
- **Semantic & ArXiv Paper Retrieval:** Finds the most relevant papers based on your query.
- **Dataset Intelligence:** Detects datasets mentioned in papers and checks their availability.
- **Research Gaps & Roadmap:** Automatically identifies unsolved problems and generates a step-by-step research plan.
- **Interactive Citation Graph:** Visualizes citations using a beautiful React Flow network.
- **Graceful Fallbacks:** The UI falls back to mock data if backend APIs are rate-limited, ensuring the dashboard always looks flawless.

---

## 🛠️ Tech Stack
- **Frontend:** Next.js 15, TypeScript, Tailwind CSS, Glassmorphism UI, React Flow
- **Backend:** FastAPI, Python, Sentence Transformers

---

## 🚀 Getting Started

The project is split into two folders: the backend (`aura-ai-research-assistant`) and the frontend (`aura-frontend`).

### 1. Setup the Backend (FastAPI)
1. Navigate to the backend folder:
   ```bash
   cd aura-ai-research-assistant
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**: 
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your `SEMANTIC_SCHOLAR_API_KEY` when you have it. (If you don't have it yet, the frontend will use fallback mock data automatically).
5. Start the backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```

### 2. Setup the Frontend (Next.js)
1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd ../aura-frontend/my-app
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔒 A Note on API Keys
Semantic Scholar enforces rate limits without an API key. If the backend fails to fetch real data due to this, the frontend is built to catch the error and automatically render realistic mock data. This means you can confidently deploy and demonstrate AURA right now without any broken UI!
