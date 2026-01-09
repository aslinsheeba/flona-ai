import { useState } from "react";

const API_BASE = "http://localhost:8000";

function App() {
    const [aRollFile, setARollFile] = useState(null);
    const [bRollFiles, setBRollFiles] = useState([]);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [similarityThreshold, setSimilarityThreshold] = useState(0.7);
    const [minGap, setMinGap] = useState(8.0);

    const handleSubmit = async () => {
        if (!aRollFile) {
            setError("Please upload an A-roll video");
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        const formData = new FormData();
        formData.append("a_roll", aRollFile);

        // Add optional params if we decide to support them in backend
        formData.append("similarity_threshold", similarityThreshold);
        formData.append("min_gap", minGap);

        bRollFiles.forEach((file) => {
            formData.append("b_rolls", file);
        });

        try {
            const response = await fetch(`${API_BASE}/process`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Processing failed");
            }

            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <header>
                <h1>🎬 AI Video Editor</h1>
                <p className="subtitle">Intelligent B-roll Placement with Semantic Reasoning</p>
            </header>

            <main>
                {/* Step 1: A-Roll */}
                <section className="card">
                    <h2>
                        <span className="step-number">1</span> A-Roll Footage
                    </h2>
                    <div className="upload-group">
                        <p className="file-info">Upload the primary "talking head" video (max 25MB for Whisper API)</p>
                        <div className="file-input-wrapper">
                            <span className={aRollFile ? "file-selected" : ""}>
                                {aRollFile ? `✓ ${aRollFile.name}` : "Click to select A-roll Video"}
                            </span>
                            <input
                                type="file"
                                accept="video/*"
                                onChange={(e) => setARollFile(e.target.files[0])}
                            />
                        </div>
                    </div>
                </section>

                {/* Step 2: B-Roll */}
                <section className="card">
                    <h2>
                        <span className="step-number">2</span> B-Roll Clips
                    </h2>
                    <div className="upload-group">
                        <p className="file-info">Collect all stock clips you want to insert</p>
                        <div className="file-input-wrapper">
                            <span className={bRollFiles.length > 0 ? "file-selected" : ""}>
                                {bRollFiles.length > 0
                                    ? `✓ ${bRollFiles.length} clips selected`
                                    : "Click to select multiple B-roll clips"}
                            </span>
                            <input
                                type="file"
                                multiple
                                accept="video/*"
                                onChange={(e) => setBRollFiles([...e.target.files])}
                            />
                        </div>
                    </div>
                </section>

                {/* Step 3: Parameters */}
                <section className="card">
                    <h2>
                        <span className="step-number">3</span> Settings
                    </h2>
                    <div className="params-grid">
                        <div className="upload-group">
                            <label>Similarity Threshold</label>
                            <input
                                type="number"
                                className="input-field"
                                min="0"
                                max="1"
                                step="0.1"
                                value={similarityThreshold}
                                onChange={(e) => setSimilarityThreshold(parseFloat(e.target.value))}
                            />
                            <small className="file-info">Higher is more strict (0.0 to 1.0)</small>
                        </div>
                        <div className="upload-group">
                            <label>Min Gap between Edits (s)</label>
                            <input
                                type="number"
                                className="input-field"
                                min="0"
                                max="60"
                                value={minGap}
                                onChange={(e) => setMinGap(parseFloat(e.target.value))}
                            />
                            <small className="file-info">Minimum seconds between B-roll clips</small>
                        </div>
                    </div>
                </section>

                {/* Action Button */}
                <div style={{ padding: "0 10px" }}>
                    <button onClick={handleSubmit} disabled={loading}>
                        {loading ? (
                            <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px" }}>
                                <span className="loading-spinner"></span> Processing AI Analysis...
                            </span>
                        ) : (
                            "🚀 Generate Edit Plan"
                        )}
                    </button>
                </div>

                {/* Error State */}
                {error && (
                    <div className="error-message">
                        <strong>Error:</strong> {error}
                    </div>
                )}

                {/* Results */}
                {result && (
                    <div className="edl-container">
                        <div className="card">
                            <h2>📋 Generated Edit Plan</h2>

                            <div className="edl-summary" style={{ background: "rgba(99, 102, 241, 0.1)", border: "1px solid rgba(99, 102, 241, 0.2)" }}>
                                <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: "10px" }}>
                                    <div>
                                        <p style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>EDITS APPLIED</p>
                                        <p style={{ fontSize: "1.5rem", fontWeight: "700" }}>{result.metadata?.edits_applied || 0}</p>
                                    </div>
                                    <div>
                                        <p style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>AVG SIMILARITY</p>
                                        <p style={{ fontSize: "1.5rem", fontWeight: "700" }}>
                                            {result.edits?.length > 0
                                                ? (result.edits.reduce((acc, curr) => acc + curr.similarity_score, 0) / result.edits.length).toFixed(2)
                                                : "0.00"}
                                        </p>
                                    </div>
                                    <div>
                                        <p style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>THRESHOLD</p>
                                        <p style={{ fontSize: "1.5rem", fontWeight: "700" }}>{similarityThreshold}</p>
                                    </div>
                                </div>
                            </div>

                            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                                {result.edits && result.edits.length > 0 ? (
                                    result.edits.map((edit, idx) => (
                                        <div key={idx} className="edit-item">
                                            <div className="edit-header">
                                                <span className="edit-time">{edit.start_time}s - {(edit.start_time + edit.duration).toFixed(2)}s</span>
                                                <span className="status-badge status-success">Match: {(edit.similarity_score * 100).toFixed(0)}%</span>
                                            </div>
                                            <p><strong>Clip:</strong> <span style={{ color: "#a5b4fc" }}>{edit.b_roll_clip}</span></p>
                                            <p style={{ fontSize: "0.9rem", marginTop: "5px" }}>"{edit.transcript_text}..."</p>
                                            <div className="edit-reason">
                                                💡 {edit.reason}
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <p className="file-info" style={{ textAlign: "center", padding: "20px" }}>
                                        No matches found above threshold. Try lowering the threshold or check your clip names.
                                    </p>
                                )}
                            </div>

                            <details style={{ marginTop: "30px" }}>
                                <summary style={{ cursor: "pointer", color: "var(--text-muted)", fontSize: "0.9rem" }}>View Raw JSON Output</summary>
                                <div style={{ marginTop: "10px" }}>
                                    <pre>{JSON.stringify(result, null, 2)}</pre>
                                </div>
                            </details>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;
