import { useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000/api/v1";

function App() {
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(false);
  const [researchResult, setResearchResult] = useState(null);
  const [error, setError] = useState("");

  const handleResearch = async (event) => {
    event.preventDefault();

    const company = companyName.trim();

    if (!company || loading) {
      return;
    }

    setLoading(true);
    setError("");
    setResearchResult(null);

    try {
      const response = await fetch(`${API_URL}/research`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          company_name: company,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to research the company."
        );
      }

      setResearchResult(data.result);
    } catch (requestError) {
      console.error("Research request failed:", requestError);

      setError(
        requestError.message ||
          "Something went wrong while researching the company."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetResearch = () => {
    setResearchResult(null);
    setError("");
    setCompanyName("");
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
        {!researchResult && !loading && (
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
                  disabled={loading}
                />
              </div>

              <button
                type="submit"
                className="research-button"
                disabled={!companyName.trim() || loading}
              >
                Research & Generate
                <span>→</span>
              </button>
            </form>

            <p className="form-hint">
              Try a company like{" "}
              <button
                type="button"
                onClick={() => setCompanyName("Razorpay")}
              >
                Razorpay
              </button>
              {" "}or{" "}
              <button
                type="button"
                onClick={() => setCompanyName("Paytm")}
              >
                Paytm
              </button>
            </p>
          </section>
        )}

        {loading && (
          <section className="loading-section">
            <div className="loading-spinner"></div>

            <p className="eyebrow">RESEARCH IN PROGRESS</p>

            <h2>
              Researching <span>{companyName}</span>
            </h2>

            <p className="loading-description">
              IntelliReach is researching the company and generating
              sales intelligence. This may take up to a minute.
            </p>

            <div className="loading-card">
              <div className="loading-row">
                <span className="loading-check">✓</span>
                <span>Running company research</span>
              </div>

              <div className="loading-row">
                <span className="loading-check">✓</span>
                <span>Analyzing business opportunities</span>
              </div>

              <div className="loading-row">
                <span className="loading-pulse"></span>
                <span>Generating personalized outreach</span>
              </div>
            </div>
          </section>
        )}

        {error && !loading && (
          <section className="error-section">
            <div className="error-icon">!</div>

            <p className="eyebrow">RESEARCH FAILED</p>

            <h2>Something went wrong</h2>

            <p>{error}</p>

            <button
              className="secondary-button"
              onClick={() => setError("")}
            >
              Try Again
            </button>
          </section>
        )}

        {researchResult && !loading && (
          <ResearchResults
            result={researchResult}
            onNewResearch={resetResearch}
          />
        )}

        {!researchResult && !loading && !error && (
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
                  Gather relevant company information, products,
                  services, technology signals, and recent developments.
                </p>
              </div>

              <div className="workflow-card">
                <div className="step-number">02</div>

                <div className="step-icon">✦</div>

                <h3>Analyze</h3>

                <p>
                  Identify realistic business pain points, AI
                  opportunities, and the strongest sales angle.
                </p>
              </div>

              <div className="workflow-card">
                <div className="step-number">03</div>

                <div className="step-icon">↗</div>

                <h3>Reach Out</h3>

                <p>
                  Generate personalized outreach and concise talking
                  points tailored to the researched company.
                </p>
              </div>
            </div>
          </section>
        )}
      </main>

      <footer>
        <span>IntelliReach</span>
        <span>AI-powered sales intelligence</span>
      </footer>
    </div>
  );
}

function ResearchResults({ result, onNewResearch }) {
  const research = result.company_research;
  const analysis = result.sales_analysis;
  const outreach = result.outreach;

  return (
    <section className="results-section">
      <div className="results-header">
        <div>
          <p className="eyebrow">RESEARCH COMPLETE</p>

          <h1>{research.company_name}</h1>

          <p>
            Company intelligence generated by IntelliReach.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={onNewResearch}
        >
          ← New Research
        </button>
      </div>

      <div className="results-grid">
        <article className="result-card overview-card">
          <div className="card-label">COMPANY OVERVIEW</div>

          <h2>What they do</h2>

          <p>{research.overview}</p>

          <div className="detail-block">
            <h3>Products & Services</h3>

            <ul>
              {research.products_services.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>

          <div className="detail-block">
            <h3>Target Market</h3>

            <p>{research.target_market}</p>
          </div>
        </article>

        <article className="result-card">
          <div className="card-label">RECENT DEVELOPMENTS</div>

          <h2>What's happening</h2>

          <ul className="result-list">
            {research.recent_developments.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="result-card">
          <div className="card-label">TECHNOLOGY SIGNALS</div>

          <h2>Technology & AI</h2>

          <ul className="result-list">
            {research.technology_signals.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="result-card pain-points-card">
          <div className="card-label">SALES INTELLIGENCE</div>

          <h2>Potential Pain Points</h2>

          <div className="pain-point-list">
            {analysis.pain_points.map((item, index) => (
              <div className="pain-point" key={index}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <p>{item}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="result-card opportunity-card">
          <div className="card-label">STRONGEST OPPORTUNITY</div>

          <h2>{analysis.strongest_opportunity}</h2>

          <p>{analysis.business_value}</p>

          <div className="hook">
            <span>OUTREACH HOOK</span>
            <p>{analysis.outreach_hook}</p>
          </div>
        </article>

        <article className="result-card outreach-card">
          <div className="card-label">PERSONALIZED OUTREACH</div>

          <h2>Ready to send</h2>

          <div className="email-box">
            {outreach.email}
          </div>

          <div className="detail-block">
            <h3>Call Talking Points</h3>

            <ol>
              {outreach.talking_points.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ol>
          </div>
        </article>
      </div>
    </section>
  );
}

export default App;