function Hero({
  companyName,
  setCompanyName,
  onResearch,
  loading,
}) {
  return (
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
        Research any company, identify business opportunities,
        and generate personalized sales outreach — all in one place.
      </p>

      <form className="research-form" onSubmit={onResearch}>
        <div className="input-wrapper">
          <span className="search-icon">⌕</span>

          <input
            type="text"
            placeholder="Enter company name..."
            value={companyName}
            onChange={(event) =>
              setCompanyName(event.target.value)
            }
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
  );
}

export default Hero;