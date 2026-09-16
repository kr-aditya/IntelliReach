function LoadingStep({
  number,
  label,
  active,
  completed,
}) {
  return (
    <div
      className={`loading-row ${
        active ? "is-active" : ""
      } ${completed ? "is-completed" : ""}`}
    >
      <span className="loading-step-number">
        {number}
      </span>

      <span className="loading-step-indicator">
        {completed ? "✓" : active ? "●" : "○"}
      </span>

      <span>{label}</span>
    </div>
  );
}

function LoadingSection({
  companyName,
  loadingStep,
}) {
  return (
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
        <LoadingStep
          number="01"
          label="Searching company information"
          active={loadingStep >= 0}
          completed={loadingStep > 0}
        />

        <LoadingStep
          number="02"
          label="Finding recent developments"
          active={loadingStep >= 1}
          completed={loadingStep > 1}
        />

        <LoadingStep
          number="03"
          label="Analyzing business opportunities"
          active={loadingStep >= 2}
          completed={loadingStep > 2}
        />

        <LoadingStep
          number="04"
          label="Generating personalized outreach"
          active={loadingStep >= 3}
          completed={false}
        />
      </div>
    </section>
  );
}

export default LoadingSection;