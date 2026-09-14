import { useState } from "react";
import "./App.css";

function App() {
  const [companyName, setCompanyName] = useState("");

  const handleResearch = (event) => {
    event.preventDefault();

    if (!companyName.trim()) {
      return;
    }

    console.log("Researching:", companyName);
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-mark">IR</div>
          <span>IntelliReach</span>
        </div>

        <div className="nav-status">
          <span className="status-dot"></span>
          AI Research Platform
        </div>
      </header>

      <main>
        <section className="hero">
          <div className="hero-badge">
            <span>✦</span>
            AI-Powered B2B Intelligence
          </div>

          <h1>
            Turn company research into
            <span> actionable outreach.</span>
          </h1>

          <p className="hero-description">
            Research any company, identify business opportunities, and
            generate personalized sales outreach — all in one place.
          </p>

          <form className="research-form" onSubmit={handleResearch}>
            <div className="input-wrapper">
              <span className="search-icon">⌕</span>

              <input
                type="text"
                placeholder="Enter company name..."
                value={companyName}
                onChange={(event) => setCompanyName(event.target.value)}
              />
            </div>

            <button
              type="submit"
              className="research-button"
              disabled={!companyName.trim()}
            >
              Research & Generate
              <span>→</span>
            </button>
          </form>

          <p className="form-hint">
            Try a company like <button type="button" onClick={() => setCompanyName("Razorpay")}>Razorpay</button>
            {" "}or{" "}
            <button type="button" onClick={() => setCompanyName("Paytm")}>Paytm</button>
          </p>
        </section>

        <section className="workflow">
          <div className="section-heading">
            <p className="eyebrow">HOW IT WORKS</p>
            <h2>From company name to sales intelligence</h2>
            <p>
              IntelliReach combines web research and AI agents to turn
              scattered information into actionable insights.
            </p>
          </div>

          <div className="workflow-grid">
            <div className="workflow-card">
              <div className="step-number">01</div>
              <div className="step-icon">⌕</div>
              <h3>Research</h3>
              <p>
                Gather relevant company information, products, services,
                technology signals, and recent developments.
              </p>
            </div>

            <div className="workflow-card">
              <div className="step-number">02</div>
              <div className="step-icon">✦</div>
              <h3>Analyze</h3>
              <p>
                Identify realistic business pain points, AI opportunities,
                and the strongest sales angle.
              </p>
            </div>

            <div className="workflow-card">
              <div className="step-number">03</div>
              <div className="step-icon">↗</div>
              <h3>Reach Out</h3>
              <p>
                Generate personalized outreach and concise talking points
                tailored to the researched company.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <span>IntelliReach</span>
        <span>AI-powered sales intelligence</span>
      </footer>
    </div>
  );
}

export default App;