import { useEffect, useState } from "react";
import "./App.css";

import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import LoadingSection from "./components/LoadingSection";
import ResearchResults from "./components/ResearchResults";
import KnowledgeBase from "./components/KnowledgeBase";

import { researchCompany } from "./services/api";

function App() {
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [researchResult, setResearchResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!loading) {
      setLoadingStep(0);
      return;
    }

    const interval = setInterval(() => {
      setLoadingStep((currentStep) => {
        if (currentStep < 3) {
          return currentStep + 1;
        }

        return currentStep;
      });
    }, 12000);

    return () => clearInterval(interval);
  }, [loading]);

  const handleResearch = async (event) => {
    event.preventDefault();

    const company = companyName.trim();

    if (!company || loading) {
      return;
    }

    setLoading(true);
    setLoadingStep(0);
    setError("");
    setResearchResult(null);

    try {
      const result = await researchCompany(company);

      setResearchResult(result);
    } catch (requestError) {
      console.error(
        "Research request failed:",
        requestError
      );

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
      <Navbar />

      <main>
        {!researchResult && !loading && (
          <Hero
            companyName={companyName}
            setCompanyName={setCompanyName}
            onResearch={handleResearch}
            loading={loading}
          />
        )}

        {loading && (
          <LoadingSection
            companyName={companyName}
            loadingStep={loadingStep}
          />
        )}

        {error && !loading && (
          <section className="error-section">
            <div className="error-icon">!</div>

            <p className="eyebrow">
              RESEARCH FAILED
            </p>

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

        {!researchResult &&
          !loading &&
          !error && (
            <section className="workflow">
              <div className="section-heading">
                <p className="eyebrow">
                  HOW IT WORKS
                </p>

                <h2>
                  From company name to sales
                  intelligence
                </h2>

                <p>
                  IntelliReach combines web
                  research and AI agents to turn
                  scattered information into
                  actionable insights.
                </p>
              </div>

              <div className="workflow-grid">
                <div className="workflow-card">
                  <div className="step-number">
                    01
                  </div>

                  <div className="step-icon">
                    ⌕
                  </div>

                  <h3>Research</h3>

                  <p>
                    Gather relevant company
                    information, products,
                    services, technology signals,
                    and recent developments.
                  </p>
                </div>

                <div className="workflow-card">
                  <div className="step-number">
                    02
                  </div>

                  <div className="step-icon">
                    ✦
                  </div>

                  <h3>Analyze</h3>

                  <p>
                    Identify realistic business
                    pain points, AI opportunities,
                    and the strongest sales angle.
                  </p>
                </div>

                <div className="workflow-card">
                  <div className="step-number">
                    03
                  </div>

                  <div className="step-icon">
                    ↗
                  </div>

                  <h3>Reach Out</h3>

                  <p>
                    Generate personalized
                    outreach and concise talking
                    points tailored to the
                    researched company.
                  </p>
                </div>
              </div>
            </section>
          )}

        <KnowledgeBase />
      </main>

      <footer>
        <span>IntelliReach</span>
        <span>
          AI-powered sales intelligence
        </span>
      </footer>
    </div>
  );
}

export default App;