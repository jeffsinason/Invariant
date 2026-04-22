import { FormEvent, ReactNode, useEffect, useMemo, useState } from "react";

import {
  fetchBenchmarks,
  fetchCases,
  fetchModels,
  fetchProviders,
  fetchRuns,
  getApiBaseUrl,
  runBenchmark,
  runCase,
} from "./api";
import type {
  BenchmarkArtifact,
  BenchmarkResultRow,
  BenchmarkRunResponse,
  CaseResultArtifact,
  CaseRunResponse,
  ModelInfo,
  ProviderInfo,
} from "./types";

type StatusTone = "danger" | "safe" | "warn" | "neutral";
type ConsoleTab = "case" | "benchmark" | "artifacts";
type BenchmarkSortMode = "risk" | "name";

function humanizeEvaluationLabel(label?: string | null): string {
  switch (label) {
    case "direct_obedience":
      return "Obeyed malicious instruction";
    case "unsafe_repetition":
      return "Repeated unsafe instruction";
    case "safe_summary":
      return "Safe summary";
    case "safe_refusal":
      return "Safe refusal";
    case "safe_other":
      return "Safe other";
    default:
      return "Not classified";
  }
}

function verdictText(vulnerable: boolean): string {
  return vulnerable ? "Vulnerable" : "Safe";
}

function verdictTone(vulnerable: boolean): StatusTone {
  return vulnerable ? "danger" : "safe";
}

function evaluationTone(label?: string | null): StatusTone {
  if (label === "direct_obedience") {
    return "danger";
  }
  if (label === "unsafe_repetition") {
    return "warn";
  }
  if (label && label.startsWith("safe_")) {
    return "safe";
  }
  return "neutral";
}

function StatusPill({
  tone,
  children,
}: {
  tone: StatusTone;
  children: ReactNode;
}) {
  return <span className={`status-pill ${tone}`}>{children}</span>;
}

function TabButton({
  active,
  children,
  onClick,
}: {
  active: boolean;
  children: ReactNode;
  onClick: () => void;
}) {
  return (
    <button className={`tab-button${active ? " active" : ""}`} type="button" onClick={onClick}>
      {children}
    </button>
  );
}

function formatJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

function formatTimestamp(value?: string | null): string {
  if (!value) {
    return "n/a";
  }

  return new Date(value).toLocaleString();
}

function artifactName(path?: string | null): string {
  if (!path) {
    return "Not saved";
  }

  return path.split("/").pop() ?? path;
}

function resultLabel(result: CaseResultArtifact): string {
  return `${result.case_name} | ${result.provider} | ${formatTimestamp(result.timestamp_utc)}`;
}

function classifyCaseFamily(caseName: string): string {
  if (caseName.startsWith("indirect_injection")) {
    return "Retrieval / Indirect Injection";
  }
  if (
    caseName.startsWith("tool_manipulation") ||
    caseName === "data_exfiltration_tool_use" ||
    caseName === "unauthorized_action_execution"
  ) {
    return "Tools / Action Abuse";
  }
  if (
    caseName === "context_poisoning" ||
    caseName === "persistent_injection" ||
    caseName === "contextual_injection" ||
    caseName === "delayed_trigger_injection"
  ) {
    return "Session / Memory";
  }
  if (
    caseName === "direct_override" ||
    caseName === "prompt_leakage" ||
    caseName === "safe_baseline" ||
    caseName === "role_confusion" ||
    caseName === "obfuscated_injection"
  ) {
    return "Core Prompt Security";
  }
  return "Other";
}

function groupResultsByFamily(results: BenchmarkResultRow[]): Array<{
  family: string;
  total: number;
  vulnerable: number;
  unsafeRepetition: number;
  rows: BenchmarkResultRow[];
}> {
  const grouped = new Map<string, BenchmarkResultRow[]>();
  for (const row of results) {
    const family = classifyCaseFamily(row.case_name);
    grouped.set(family, [...(grouped.get(family) ?? []), row]);
  }

  return Array.from(grouped.entries()).map(([family, rows]) => ({
    family,
    total: rows.length,
    vulnerable: rows.filter((row) => row.vulnerable).length,
    unsafeRepetition: rows.filter((row) => row.evaluation_label === "unsafe_repetition").length,
    rows: rows.sort((left, right) => left.case_name.localeCompare(right.case_name)),
  }));
}

function summarizeBenchmarkClasses(report: BenchmarkArtifact) {
  return {
    directObedience: report.results.filter((item) => item.evaluation_label === "direct_obedience").length,
    unsafeRepetition: report.results.filter((item) => item.evaluation_label === "unsafe_repetition").length,
    safeClassified: report.results.filter((item) => item.evaluation_label?.startsWith("safe_")).length,
  };
}

function summarizeRisk(result: CaseResultArtifact): string {
  if (result.evaluation_label === "direct_obedience") {
    return "High risk. The model followed malicious content from the prompt or retrieved material.";
  }
  if (result.evaluation_label === "unsafe_repetition") {
    return "Medium risk. The model echoed malicious content into the answer path without full compliance.";
  }
  if (result.vulnerable) {
    return "High risk. The case evaluator marked this response as vulnerable.";
  }
  if (result.evaluation_label?.startsWith("safe_")) {
    return "Low risk. The model stayed on task or refused the malicious instruction.";
  }
  return "Low risk. No vulnerability was detected in this run.";
}

function explainCaseResult(result: CaseResultArtifact): string[] {
  const findings: string[] = [];

  if (result.evaluation_label === "direct_obedience") {
    findings.push("The model complied with the malicious instruction instead of staying on the requested task.");
  } else if (result.evaluation_label === "unsafe_repetition") {
    findings.push("The model echoed malicious content back into the answer path, which can still leak or amplify unsafe instructions.");
  } else if (result.evaluation_label === "safe_summary") {
    findings.push("The model stayed on the benign task and summarized the non-malicious content.");
  } else if (result.evaluation_label === "safe_refusal") {
    findings.push("The model explicitly refused to follow the malicious instruction.");
  }

  findings.push(`This case belongs to the ${classifyCaseFamily(result.case_name)} family.`);

  if (result.tool_calls?.length) {
    findings.push(`The model produced ${result.tool_calls.length} tool call${result.tool_calls.length === 1 ? "" : "s"} during this run.`);
  }

  if (result.error_type) {
    findings.push(`The run also recorded an error: ${result.error_type}.`);
  }

  return findings;
}

function topBenchmarkFindings(report: BenchmarkArtifact): string[] {
  const vulnerable = report.results.filter((item) => item.vulnerable);
  const unsafeEcho = report.results.filter((item) => item.evaluation_label === "unsafe_repetition");
  const findings: string[] = [];

  if (vulnerable.length > 0) {
    findings.push(
      `${vulnerable.length} case${vulnerable.length === 1 ? "" : "s"} showed direct obedience: ${vulnerable
        .slice(0, 3)
        .map((item) => item.case_name)
        .join(", ")}${vulnerable.length > 3 ? ", ..." : ""}.`,
    );
  }

  if (unsafeEcho.length > 0) {
    findings.push(
      `${unsafeEcho.length} case${unsafeEcho.length === 1 ? "" : "s"} showed unsafe echoing without full compliance.`,
    );
  }

  if (findings.length === 0) {
    findings.push("No vulnerabilities detected in this benchmark snapshot.");
  }

  return findings;
}

function sortResults(rows: BenchmarkResultRow[], mode: BenchmarkSortMode): BenchmarkResultRow[] {
  if (mode === "name") {
    return [...rows].sort((left, right) => left.case_name.localeCompare(right.case_name));
  }

  const riskRank = (row: BenchmarkResultRow) => {
    if (row.evaluation_label === "direct_obedience") {
      return 0;
    }
    if (row.evaluation_label === "unsafe_repetition") {
      return 1;
    }
    if (row.vulnerable) {
      return 2;
    }
    return 3;
  };

  return [...rows].sort((left, right) => {
    const riskDelta = riskRank(left) - riskRank(right);
    if (riskDelta !== 0) {
      return riskDelta;
    }
    return left.case_name.localeCompare(right.case_name);
  });
}

function compareCaseResults(left: CaseResultArtifact | null, right: CaseResultArtifact | null) {
  if (!left || !right) {
    return [];
  }

  return [
    { label: "Case", left: left.case_name, right: right.case_name },
    { label: "Provider", left: left.provider, right: right.provider },
    { label: "Model", left: left.model_name, right: right.model_name },
    { label: "Verdict", left: verdictText(left.vulnerable), right: verdictText(right.vulnerable) },
    {
      label: "Response Class",
      left: humanizeEvaluationLabel(left.evaluation_label),
      right: humanizeEvaluationLabel(right.evaluation_label),
    },
    { label: "Stop Reason", left: left.stop_reason ?? "n/a", right: right.stop_reason ?? "n/a" },
    {
      label: "Tool Calls",
      left: String(left.tool_calls?.length ?? 0),
      right: String(right.tool_calls?.length ?? 0),
    },
    {
      label: "Input Tokens",
      left: String((left.usage as { input_tokens?: number } | null)?.input_tokens ?? "n/a"),
      right: String((right.usage as { input_tokens?: number } | null)?.input_tokens ?? "n/a"),
    },
    {
      label: "Output Tokens",
      left: String((left.usage as { output_tokens?: number } | null)?.output_tokens ?? "n/a"),
      right: String((right.usage as { output_tokens?: number } | null)?.output_tokens ?? "n/a"),
    },
  ];
}

function ArtifactDetail({
  title,
  result,
  benchmark,
}: {
  title: string;
  result?: CaseResultArtifact | null;
  benchmark?: BenchmarkArtifact | null;
}) {
  return (
    <div className="panel detail-panel">
      <div className="panel-heading">
        <h2>{title}</h2>
        <p>Full artifact drilldown for the selected item.</p>
      </div>

      {result ? (
        <>
          <div className="summary-strip drilldown-summary">
            <div className="summary-card">
              <span>Case</span>
              <strong>{result.case_name}</strong>
            </div>
            <div className="summary-card">
              <span>Verdict</span>
              <strong>{verdictText(result.vulnerable)}</strong>
            </div>
            <div className="summary-card">
              <span>Response Class</span>
              <strong>{humanizeEvaluationLabel(result.evaluation_label)}</strong>
            </div>
          </div>
          <dl className="detail-grid">
            <div><dt>Case</dt><dd>{result.case_name}</dd></div>
            <div><dt>Provider</dt><dd>{result.provider}</dd></div>
            <div><dt>Model</dt><dd>{result.model_name}</dd></div>
            <div><dt>Verdict</dt><dd><StatusPill tone={verdictTone(result.vulnerable)}>{verdictText(result.vulnerable)}</StatusPill></dd></div>
            <div><dt>Response Class</dt><dd><StatusPill tone={evaluationTone(result.evaluation_label)}>{humanizeEvaluationLabel(result.evaluation_label)}</StatusPill></dd></div>
            <div><dt>Timestamp</dt><dd>{formatTimestamp(result.timestamp_utc)}</dd></div>
            <div><dt>Artifact</dt><dd>{artifactName(result.saved_path ?? result.artifact_path)}</dd></div>
          </dl>
          <div className="insight-banner">
            <strong>Operator Summary</strong>
            <span>{summarizeRisk(result)}</span>
          </div>
          <h3>Why This Result Landed Here</h3>
          <ul className="plain-list compact-list">
            {explainCaseResult(result).map((finding) => (
              <li key={finding}>{finding}</li>
            ))}
          </ul>
          <h3>Response</h3>
          <pre>{result.response_text || "(empty response)"}</pre>
          <h3>Notes</h3>
          <pre>{result.notes || "(no notes)"}</pre>
          <details className="technical-section">
            <summary>Technical Metadata</summary>
            <pre>{formatJson({
              evaluation_label: result.evaluation_label,
              request_id: result.request_id,
              stop_reason: result.stop_reason,
              usage: result.usage,
              tool_calls: result.tool_calls,
              error_type: result.error_type,
              error_message: result.error_message,
            })}</pre>
          </details>
          <details className="technical-section">
            <summary>Raw Provider Response</summary>
            <pre>{formatJson(result.raw_response)}</pre>
          </details>
        </>
      ) : null}

      {benchmark ? (
        <>
          <div className="summary-strip drilldown-summary">
            <div className="summary-card">
              <span>Provider</span>
              <strong>{benchmark.provider}</strong>
            </div>
            <div className="summary-card">
              <span>Vulnerable Cases</span>
              <strong>{benchmark.summary.vulnerable_cases}</strong>
            </div>
            <div className="summary-card">
              <span>Cases in Scope</span>
              <strong>{benchmark.summary.total_cases}</strong>
            </div>
          </div>
          <dl className="detail-grid">
            <div><dt>Provider</dt><dd>{benchmark.provider}</dd></div>
            <div><dt>Model</dt><dd>{benchmark.model_name}</dd></div>
            <div><dt>Total</dt><dd>{benchmark.summary.total_cases}</dd></div>
            <div><dt>Vulnerable</dt><dd>{benchmark.summary.vulnerable_cases}</dd></div>
            <div><dt>Safe</dt><dd>{benchmark.summary.safe_cases}</dd></div>
            <div><dt>Generated</dt><dd>{formatTimestamp(benchmark.generated_at_utc)}</dd></div>
          </dl>
          <div className="insight-banner">
            <strong>Key Findings</strong>
            <ul className="plain-list compact-list">
              {topBenchmarkFindings(benchmark).map((finding) => (
                <li key={finding}>{finding}</li>
              ))}
            </ul>
          </div>
          <h3>Family Breakdown</h3>
          <div className="family-stack">
            {groupResultsByFamily(benchmark.results).map((group) => (
              <section key={group.family} className="family-card">
                <div className="family-header">
                  <div>
                    <strong>{group.family}</strong>
                    <span>{group.total} cases</span>
                  </div>
                  <div className="family-metrics">
                    <StatusPill tone={group.vulnerable > 0 ? "danger" : "safe"}>
                      {group.vulnerable} vulnerable
                    </StatusPill>
                    <StatusPill tone={group.unsafeRepetition > 0 ? "warn" : "neutral"}>
                      {group.unsafeRepetition} unsafe echo
                    </StatusPill>
                  </div>
                </div>
              </section>
            ))}
          </div>
          <details className="technical-section">
            <summary>Raw Benchmark Payload</summary>
            <pre>{formatJson(benchmark.results)}</pre>
          </details>
        </>
      ) : null}

      {!result && !benchmark ? <p className="empty-state">Select a run or benchmark artifact to inspect it here.</p> : null}
    </div>
  );
}

function ComparisonTable({
  left,
  right,
}: {
  left: CaseResultArtifact | null;
  right: CaseResultArtifact | null;
}) {
  const rows = compareCaseResults(left, right);

  return (
    <div className="panel detail-panel">
      <div className="panel-heading">
        <h2>Provider Comparison</h2>
        <p>Side-by-side view of two saved run artifacts.</p>
      </div>

      {left && right ? (
        <>
          <div className="comparison-head">
            <div>
              <strong>{left.provider}</strong>
              <span>{left.model_name}</span>
              <StatusPill tone={verdictTone(left.vulnerable)}>{verdictText(left.vulnerable)}</StatusPill>
            </div>
            <div>
              <strong>{right.provider}</strong>
              <span>{right.model_name}</span>
              <StatusPill tone={verdictTone(right.vulnerable)}>{verdictText(right.vulnerable)}</StatusPill>
            </div>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Dimension</th>
                  <th>{left.provider}</th>
                  <th>{right.provider}</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.label}>
                    <td>{row.label}</td>
                    <td>{row.left}</td>
                    <td>{row.right}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <h3>Response Comparison</h3>
          <div className="comparison-columns">
            <pre>{left.response_text || "(empty response)"}</pre>
            <pre>{right.response_text || "(empty response)"}</pre>
          </div>
        </>
      ) : (
        <p className="empty-state">Choose two run artifacts below to compare them here.</p>
      )}
    </div>
  );
}

function BenchmarkSummaryTable({
  report,
  familyFilter,
  sortMode,
  title,
}: {
  report: BenchmarkArtifact | null;
  familyFilter: string;
  sortMode: BenchmarkSortMode;
  title: string;
}) {
  const filteredResults = report
    ? report.results.filter((item) => familyFilter === "all" || classifyCaseFamily(item.case_name) === familyFilter)
    : [];
  const familyGroups = report ? groupResultsByFamily(sortResults(filteredResults, sortMode)) : [];
  const classSummary = report ? summarizeBenchmarkClasses(report) : null;

  return (
    <div className="panel detail-panel">
      <div className="panel-heading">
        <h2>{title}</h2>
        <p>Benchmark summary grouped by attack family.</p>
      </div>
      {report ? (
        <>
          <dl className="detail-grid">
            <div><dt>Provider</dt><dd>{report.provider}</dd></div>
            <div><dt>Model</dt><dd>{report.model_name}</dd></div>
            <div><dt>Total</dt><dd>{report.summary.total_cases}</dd></div>
            <div><dt>Vulnerable</dt><dd>{report.summary.vulnerable_cases}</dd></div>
            <div><dt>Safe</dt><dd>{report.summary.safe_cases}</dd></div>
            <div><dt>Generated</dt><dd>{formatTimestamp(report.generated_at_utc)}</dd></div>
          </dl>
          <div className="summary-strip">
            <div className="summary-card">
              <span>Obeyed malicious instruction</span>
              <strong>{classSummary?.directObedience ?? 0}</strong>
            </div>
            <div className="summary-card">
              <span>Repeated unsafe instruction</span>
              <strong>{classSummary?.unsafeRepetition ?? 0}</strong>
            </div>
            <div className="summary-card">
              <span>Safe summary or refusal</span>
              <strong>{classSummary?.safeClassified ?? 0}</strong>
            </div>
          </div>
          <h3>Family Breakdown</h3>
          <div className="family-stack">
            {familyGroups.map((group) => (
              <section key={group.family} className="family-card">
                <div className="family-header">
                  <div>
                    <strong>{group.family}</strong>
                    <span>{group.total} cases</span>
                  </div>
                  <div className="family-metrics">
                    <StatusPill tone={group.vulnerable > 0 ? "danger" : "safe"}>
                      {group.vulnerable} vulnerable
                    </StatusPill>
                    <StatusPill tone={group.unsafeRepetition > 0 ? "warn" : "neutral"}>
                      {group.unsafeRepetition} unsafe echo
                    </StatusPill>
                  </div>
                </div>
                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>Case</th>
                        <th>Verdict</th>
                        <th>Response Class</th>
                        <th>Tools</th>
                      </tr>
                    </thead>
                    <tbody>
                      {group.rows.map((item) => (
                        <tr key={`${item.case_name}-${item.timestamp_utc}`}>
                          <td>{item.case_name}</td>
                          <td><StatusPill tone={verdictTone(item.vulnerable)}>{verdictText(item.vulnerable)}</StatusPill></td>
                          <td><StatusPill tone={evaluationTone(item.evaluation_label)}>{humanizeEvaluationLabel(item.evaluation_label)}</StatusPill></td>
                          <td>{item.tool_call_count}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            ))}
          </div>
        </>
      ) : (
        <p className="empty-state">Run a benchmark to inspect the report here.</p>
      )}
    </div>
  );
}

function BenchmarkComparisonTable({
  left,
  right,
}: {
  left: BenchmarkArtifact | null;
  right: BenchmarkArtifact | null;
}) {
  if (!left || !right) {
    return (
      <div className="panel detail-panel">
        <div className="panel-heading">
          <h2>Benchmark Comparison</h2>
          <p>Select two benchmark artifacts to compare them here.</p>
        </div>
        <p className="empty-state">Choose two saved benchmark artifacts in this tab.</p>
      </div>
    );
  }

  const leftRows = new Map(left.results.map((row) => [row.case_name, row]));
  const sharedCases = right.results
    .filter((row) => leftRows.has(row.case_name))
    .map((row) => {
      const leftRow = leftRows.get(row.case_name)!;
      return {
        case_name: row.case_name,
        left: leftRow,
        right: row,
        changed:
          leftRow.vulnerable !== row.vulnerable ||
          leftRow.evaluation_label !== row.evaluation_label,
      };
    })
    .sort((a, b) => Number(b.changed) - Number(a.changed) || a.case_name.localeCompare(b.case_name));

  return (
    <div className="panel detail-panel">
      <div className="panel-heading">
        <h2>Benchmark Comparison</h2>
        <p>Side-by-side comparison of two saved benchmark artifacts.</p>
      </div>
      <div className="comparison-head">
        <div>
          <strong>{left.provider}</strong>
          <span>{left.model_name}</span>
          <StatusPill tone={left.summary.vulnerable_cases > 0 ? "danger" : "safe"}>
            {left.summary.vulnerable_cases} vulnerable
          </StatusPill>
        </div>
        <div>
          <strong>{right.provider}</strong>
          <span>{right.model_name}</span>
          <StatusPill tone={right.summary.vulnerable_cases > 0 ? "danger" : "safe"}>
            {right.summary.vulnerable_cases} vulnerable
          </StatusPill>
        </div>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Case</th>
              <th>{left.provider}</th>
              <th>{right.provider}</th>
              <th>Changed</th>
            </tr>
          </thead>
          <tbody>
            {sharedCases.map((row) => (
              <tr key={row.case_name}>
                <td>{row.case_name}</td>
                <td>{verdictText(row.left.vulnerable)} · {humanizeEvaluationLabel(row.left.evaluation_label)}</td>
                <td>{verdictText(row.right.vulnerable)} · {humanizeEvaluationLabel(row.right.evaluation_label)}</td>
                <td>
                  <StatusPill tone={row.changed ? "warn" : "neutral"}>
                    {row.changed ? "Yes" : "No"}
                  </StatusPill>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ProviderDifferencesPanel({
  currentReport,
  benchmarks,
}: {
  currentReport: BenchmarkArtifact | null;
  benchmarks: BenchmarkArtifact[];
}) {
  const focused = currentReport ?? benchmarks[0] ?? null;

  const providerSnapshots = useMemo(() => {
    const latestByProvider = new Map<string, BenchmarkArtifact>();
    for (const benchmark of benchmarks) {
      if (!latestByProvider.has(benchmark.provider)) {
        latestByProvider.set(benchmark.provider, benchmark);
      }
    }
    return Array.from(latestByProvider.values());
  }, [benchmarks]);

  const focusedRows = new Map((focused?.results ?? []).map((row) => [row.case_name, row]));

  return (
    <div className="panel detail-panel">
      <div className="panel-heading">
        <h2>Provider Differences</h2>
        <p>Latest benchmark snapshot by provider, anchored on the current report.</p>
      </div>
      {focused ? (
        <>
          <div className="summary-strip provider-strip">
            {providerSnapshots.map((benchmark) => (
              <div key={`${benchmark.provider}-${benchmark.generated_at_utc}`} className="summary-card">
                <span>{benchmark.provider}</span>
                <strong>{benchmark.summary.vulnerable_cases} vulnerable</strong>
                <span>{benchmark.model_name}</span>
              </div>
            ))}
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Provider</th>
                  <th>Model</th>
                  <th>Vulnerable</th>
                  <th>Unsafe Echo</th>
                  <th>Delta vs {focused.provider}</th>
                </tr>
              </thead>
              <tbody>
                {providerSnapshots.map((benchmark) => {
                  const vulnerableCount = benchmark.results.filter((item) => item.vulnerable).length;
                  const unsafeEchoCount = benchmark.results.filter((item) => item.evaluation_label === "unsafe_repetition").length;
                  const comparableCases = benchmark.results.filter((item) => focusedRows.has(item.case_name));
                  const delta = comparableCases.reduce((count, item) => {
                    const focusedRow = focusedRows.get(item.case_name);
                    if (!focusedRow) {
                      return count;
                    }
                    return count + (item.vulnerable !== focusedRow.vulnerable ? 1 : 0);
                  }, 0);

                  return (
                    <tr key={`${benchmark.provider}-${benchmark.generated_at_utc}`}>
                      <td>{benchmark.provider}</td>
                      <td>{benchmark.model_name}</td>
                      <td><StatusPill tone={vulnerableCount > 0 ? "danger" : "safe"}>{vulnerableCount}</StatusPill></td>
                      <td><StatusPill tone={unsafeEchoCount > 0 ? "warn" : "neutral"}>{unsafeEchoCount}</StatusPill></td>
                      <td>{delta} case{delta === 1 ? "" : "s"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <p className="empty-state">Run or select a benchmark to compare providers here.</p>
      )}
    </div>
  );
}

export function App() {
  const [providers, setProviders] = useState<ProviderInfo[]>([]);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [cases, setCases] = useState<string[]>([]);
  const [runs, setRuns] = useState<CaseResultArtifact[]>([]);
  const [benchmarks, setBenchmarks] = useState<BenchmarkArtifact[]>([]);
  const [provider, setProvider] = useState("mock");
  const [modelName, setModelName] = useState("");
  const [useCustomModelName, setUseCustomModelName] = useState(false);
  const [showAllCaseModels, setShowAllCaseModels] = useState(false);
  const [benchmarkProvider, setBenchmarkProvider] = useState("mock");
  const [benchmarkModelName, setBenchmarkModelName] = useState("");
  const [useCustomBenchmarkModelName, setUseCustomBenchmarkModelName] = useState(false);
  const [showAllBenchmarkModels, setShowAllBenchmarkModels] = useState(false);
  const [caseName, setCaseName] = useState("");
  const [selectedBenchmarkCases, setSelectedBenchmarkCases] = useState<string[]>([]);
  const [saveArtifacts, setSaveArtifacts] = useState(true);
  const [activeTab, setActiveTab] = useState<ConsoleTab>("case");
  const [currentRunDetail, setCurrentRunDetail] = useState<CaseResultArtifact | null>(null);
  const [currentBenchmarkDetail, setCurrentBenchmarkDetail] = useState<BenchmarkArtifact | null>(null);
  const [selectedRunDetail, setSelectedRunDetail] = useState<CaseResultArtifact | null>(null);
  const [selectedBenchmarkDetail, setSelectedBenchmarkDetail] = useState<BenchmarkArtifact | null>(null);
  const [comparisonLeft, setComparisonLeft] = useState<string>("");
  const [comparisonRight, setComparisonRight] = useState<string>("");
  const [benchmarkComparisonLeft, setBenchmarkComparisonLeft] = useState<string>("");
  const [benchmarkComparisonRight, setBenchmarkComparisonRight] = useState<string>("");
  const [currentBenchmarkFamilyFilter, setCurrentBenchmarkFamilyFilter] = useState<string>("all");
  const [selectedBenchmarkFamilyFilter, setSelectedBenchmarkFamilyFilter] = useState<string>("all");
  const [currentBenchmarkSortMode, setCurrentBenchmarkSortMode] = useState<BenchmarkSortMode>("risk");
  const [selectedBenchmarkSortMode, setSelectedBenchmarkSortMode] = useState<BenchmarkSortMode>("risk");
  const [loading, setLoading] = useState(true);
  const [runningCase, setRunningCase] = useState(false);
  const [runningBenchmark, setRunningBenchmark] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    async function loadInitialState() {
      try {
        const [providerData, caseData, runData, benchmarkData] = await Promise.all([
          fetchProviders(),
          fetchCases(),
          fetchRuns(),
          fetchBenchmarks(),
        ]);
        const modelData = await fetchModels();

        setProviders(providerData);
        setModels(modelData);
        setCases(caseData);
        setRuns(runData);
        setBenchmarks(benchmarkData);

        const initialProvider = providerData[0]?.provider ?? "mock";
        setProvider(initialProvider);
        setModelName(providerData[0]?.default_model ?? "");
        setBenchmarkProvider(initialProvider);
        setBenchmarkModelName(providerData[0]?.default_model ?? "");
        setCaseName(caseData[0] ?? "");
        setSelectedBenchmarkCases(caseData);
        setSelectedRunDetail(runData[0] ?? null);
        setSelectedBenchmarkDetail(benchmarkData[0] ?? null);
        setComparisonLeft(runData[0]?.artifact_path ?? "");
        setComparisonRight(runData[1]?.artifact_path ?? runData[0]?.artifact_path ?? "");
        setBenchmarkComparisonLeft(benchmarkData[0]?.artifact_path ?? "");
        setBenchmarkComparisonRight(benchmarkData[1]?.artifact_path ?? benchmarkData[0]?.artifact_path ?? "");
      } catch (error) {
        setErrorMessage(error instanceof Error ? error.message : "Failed to load console data.");
      } finally {
        setLoading(false);
      }
    }

    void loadInitialState();
  }, []);

  useEffect(() => {
    const selectedProvider = providers.find((item) => item.provider === provider);
    if (selectedProvider && !modelName && !useCustomModelName) {
      setModelName(selectedProvider.default_model);
    }
  }, [provider, providers, modelName, useCustomModelName]);

  useEffect(() => {
    const selectedProvider = providers.find((item) => item.provider === benchmarkProvider);
    if (selectedProvider && !benchmarkModelName && !useCustomBenchmarkModelName) {
      setBenchmarkModelName(selectedProvider.default_model);
    }
  }, [benchmarkProvider, providers, benchmarkModelName, useCustomBenchmarkModelName]);

  const caseModelsForProvider = useMemo(
    () => {
      const providerModels = models.filter((item) => item.provider === provider);
      if (showAllCaseModels) {
        return providerModels;
      }
      return providerModels.filter((item) => item.recommended_for_harness);
    },
    [models, provider, showAllCaseModels],
  );
  const benchmarkModelsForProvider = useMemo(
    () => {
      const providerModels = models.filter((item) => item.provider === benchmarkProvider);
      if (showAllBenchmarkModels) {
        return providerModels;
      }
      return providerModels.filter((item) => item.recommended_for_harness);
    },
    [models, benchmarkProvider, showAllBenchmarkModels],
  );
  const leftComparisonRun = useMemo(
    () => runs.find((item) => item.artifact_path === comparisonLeft) ?? null,
    [comparisonLeft, runs],
  );
  const rightComparisonRun = useMemo(
    () => runs.find((item) => item.artifact_path === comparisonRight) ?? null,
    [comparisonRight, runs],
  );
  const leftComparisonBenchmark = useMemo(
    () => benchmarks.find((item) => item.artifact_path === benchmarkComparisonLeft) ?? null,
    [benchmarkComparisonLeft, benchmarks],
  );
  const rightComparisonBenchmark = useMemo(
    () => benchmarks.find((item) => item.artifact_path === benchmarkComparisonRight) ?? null,
    [benchmarkComparisonRight, benchmarks],
  );
  const currentBenchmarkFamilyOptions = useMemo(() => {
    if (!currentBenchmarkDetail) {
      return ["all"];
    }
    return ["all", ...Array.from(new Set(currentBenchmarkDetail.results.map((item) => classifyCaseFamily(item.case_name))))];
  }, [currentBenchmarkDetail]);
  const selectedBenchmarkFamilyOptions = useMemo(() => {
    if (!selectedBenchmarkDetail) {
      return ["all"];
    }
    return ["all", ...Array.from(new Set(selectedBenchmarkDetail.results.map((item) => classifyCaseFamily(item.case_name))))];
  }, [selectedBenchmarkDetail]);

  async function refreshArtifacts() {
    const [runData, benchmarkData] = await Promise.all([fetchRuns(), fetchBenchmarks()]);
    setRuns(runData);
    setBenchmarks(benchmarkData);
    setSelectedRunDetail((current) => current ? runData.find((item) => item.artifact_path === current.artifact_path) ?? runData[0] ?? null : runData[0] ?? null);
    setSelectedBenchmarkDetail((current) => current ? benchmarkData.find((item) => item.artifact_path === current.artifact_path) ?? benchmarkData[0] ?? null : benchmarkData[0] ?? null);
    setComparisonLeft((current) => current || runData[0]?.artifact_path || "");
    setComparisonRight((current) => current || runData[1]?.artifact_path || runData[0]?.artifact_path || "");
    setBenchmarkComparisonLeft((current) => current || benchmarkData[0]?.artifact_path || "");
    setBenchmarkComparisonRight((current) => current || benchmarkData[1]?.artifact_path || benchmarkData[0]?.artifact_path || "");
  }

  async function handleRunCase(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRunningCase(true);
    setErrorMessage(null);

    try {
      const response: CaseRunResponse = await runCase({
        case_name: caseName,
        provider,
        model_name: modelName,
        save: saveArtifacts,
      });
      setCurrentRunDetail(response.result);
      setSelectedRunDetail(response.result);
      setActiveTab("case");
      await refreshArtifacts();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Case run failed.");
    } finally {
      setRunningCase(false);
    }
  }

  async function handleRunBenchmark(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRunningBenchmark(true);
    setErrorMessage(null);

    try {
      const response: BenchmarkRunResponse = await runBenchmark({
        provider: benchmarkProvider,
        model_name: benchmarkModelName,
        case_names: selectedBenchmarkCases,
        save: saveArtifacts,
      });
      setCurrentBenchmarkDetail(response.report);
      setSelectedBenchmarkDetail(response.report);
      setActiveTab("benchmark");
      await refreshArtifacts();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Benchmark run failed.");
    } finally {
      setRunningBenchmark(false);
    }
  }

  function handleToggleBenchmarkCase(targetCase: string) {
    setSelectedBenchmarkCases((current) =>
      current.includes(targetCase)
        ? current.filter((item) => item !== targetCase)
        : [...current, targetCase],
    );
  }

  function handleSelectAllBenchmarkCases() {
    setSelectedBenchmarkCases(cases);
  }

  function handleClearBenchmarkCases() {
    setSelectedBenchmarkCases([]);
  }

  if (loading) {
    return <main className="shell"><p>Loading Invariant console...</p></main>;
  }

  return (
    <main className="shell">
      <section className="header-band">
        <div>
          <p className="eyebrow">EchoForgeX / Invariant</p>
          <h1>Invariant Operator Console</h1>
          <p className="subtitle">
            Run injection cases, inspect benchmark artifacts, and compare provider behavior
            without leaving the harness.
          </p>
        </div>
        <div className="status-stack">
          <div className="status-chip">API: {getApiBaseUrl()}</div>
          <div className="status-chip">Cases: {cases.length}</div>
          <div className="status-chip">Providers: {providers.length}</div>
        </div>
      </section>

      {errorMessage ? <section className="alert error">{errorMessage}</section> : null}

      <section className="tab-row">
        <TabButton active={activeTab === "case"} onClick={() => setActiveTab("case")}>
          Run Case
        </TabButton>
        <TabButton active={activeTab === "benchmark"} onClick={() => setActiveTab("benchmark")}>
          Run Benchmark
        </TabButton>
        <TabButton active={activeTab === "artifacts"} onClick={() => setActiveTab("artifacts")}>
          Artifacts
        </TabButton>
      </section>

      {activeTab === "case" ? (
        <>
          <section className="grid two-up">
            <form className="panel" onSubmit={handleRunCase}>
              <div className="panel-heading">
                <h2>Run Case</h2>
                <p>Single-case execution against one provider and model.</p>
              </div>

              <label>
                Provider
                <select
                  value={provider}
                  onChange={(event) => {
                    const nextProvider = event.target.value;
                    setProvider(nextProvider);
                    const nextDefaultModel =
                      providers.find((item) => item.provider === nextProvider)?.default_model ?? "";
                    setModelName(nextDefaultModel);
                    setUseCustomModelName(false);
                    setShowAllCaseModels(false);
                  }}
                >
                  {providers.map((item) => (
                    <option key={item.provider} value={item.provider}>
                      {item.provider}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Model
                <select
                  value={modelName}
                  onChange={(event) => setModelName(event.target.value)}
                  disabled={useCustomModelName}
                >
                  {caseModelsForProvider.map((item) => (
                    <option key={`${item.provider}-${item.id}`} value={item.id}>
                      {item.display_name} ({item.id})
                    </option>
                  ))}
                </select>
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  checked={showAllCaseModels}
                  onChange={(event) => setShowAllCaseModels(event.target.checked)}
                />
                Show all available models
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  checked={useCustomModelName}
                  onChange={(event) => {
                    const checked = event.target.checked;
                    setUseCustomModelName(checked);
                    if (!checked) {
                      const defaultModel =
                        providers.find((item) => item.provider === provider)?.default_model ?? "";
                      setModelName(defaultModel);
                    }
                  }}
                />
                Use custom model id
              </label>

              <label>
                Custom model id
                <input
                  value={modelName}
                  onChange={(event) => setModelName(event.target.value)}
                  disabled={!useCustomModelName}
                />
              </label>

              <label>
                Case
                <select value={caseName} onChange={(event) => setCaseName(event.target.value)}>
                  {cases.map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  ))}
                </select>
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  checked={saveArtifacts}
                  onChange={(event) => setSaveArtifacts(event.target.checked)}
                />
                Save artifact JSON
              </label>

              <button className="button-primary" type="submit" disabled={runningCase || !caseName}>
                {runningCase ? "Running case..." : "Run case"}
              </button>
            </form>

            <ArtifactDetail title="Current Run Case" result={currentRunDetail} />
          </section>

          <section className="grid full-width">
            <div className="panel-stack">
              <div className="panel detail-panel">
                <div className="panel-heading">
                  <h2>Selected Case Result</h2>
                  <p>Choose a saved run artifact to inspect without changing the current run panel.</p>
                </div>
                <label>
                  Saved run
                  <select
                    value={selectedRunDetail?.artifact_path ?? ""}
                    onChange={(event) => {
                      const selected = runs.find((item) => item.artifact_path === event.target.value) ?? null;
                      setSelectedRunDetail(selected);
                    }}
                  >
                    {runs.map((item) => (
                      <option key={`selected-run-${item.artifact_path ?? item.timestamp_utc}`} value={item.artifact_path}>
                        {resultLabel(item)}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
              <ArtifactDetail title="Selected Case Result" result={selectedRunDetail} />
            </div>
          </section>
        </>
      ) : null}

      {activeTab === "benchmark" ? (
        <>
          <section className="grid full-width">
            <form className="panel compact-run-panel compact-benchmark-form" onSubmit={handleRunBenchmark}>
              <div className="panel-heading">
                <h2>Run Benchmark</h2>
                <p>Run a new benchmark, then compare it against saved benchmarks below.</p>
              </div>

              <div className="benchmark-form-grid">
                <label>
                  Provider
                  <select
                    value={benchmarkProvider}
                    onChange={(event) => {
                      const nextProvider = event.target.value;
                      setBenchmarkProvider(nextProvider);
                      const nextDefaultModel =
                        providers.find((item) => item.provider === nextProvider)?.default_model ?? "";
                      setBenchmarkModelName(nextDefaultModel);
                      setUseCustomBenchmarkModelName(false);
                      setShowAllBenchmarkModels(false);
                    }}
                  >
                    {providers.map((item) => (
                      <option key={`benchmark-provider-${item.provider}`} value={item.provider}>
                        {item.provider}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Model
                  <select
                    value={benchmarkModelName}
                    onChange={(event) => setBenchmarkModelName(event.target.value)}
                    disabled={useCustomBenchmarkModelName}
                  >
                    {benchmarkModelsForProvider.map((item) => (
                      <option key={`benchmark-${item.provider}-${item.id}`} value={item.id}>
                        {item.display_name} ({item.id})
                      </option>
                    ))}
                  </select>
                </label>

                <label className="checkbox-row compact-checkbox">
                  <input
                    type="checkbox"
                    checked={showAllBenchmarkModels}
                    onChange={(event) => setShowAllBenchmarkModels(event.target.checked)}
                  />
                  Show all available models
                </label>

                <label className="checkbox-row compact-checkbox">
                  <input
                    type="checkbox"
                    checked={useCustomBenchmarkModelName}
                    onChange={(event) => {
                      const checked = event.target.checked;
                      setUseCustomBenchmarkModelName(checked);
                      if (!checked) {
                        const defaultModel =
                          providers.find((item) => item.provider === benchmarkProvider)?.default_model ?? "";
                        setBenchmarkModelName(defaultModel);
                      }
                    }}
                  />
                  Use custom model id
                </label>
              </div>

              {useCustomBenchmarkModelName ? (
                <label className="compact-field">
                  Custom model id
                  <input
                    value={benchmarkModelName}
                    onChange={(event) => setBenchmarkModelName(event.target.value)}
                    disabled={!useCustomBenchmarkModelName}
                  />
                </label>
              ) : null}

              <div className="benchmark-run-footer">
                <div className="benchmark-case-summary">
                  <span>{selectedBenchmarkCases.length} selected</span>
                  <div className="inline-actions">
                    <button className="button-secondary" type="button" onClick={handleSelectAllBenchmarkCases}>
                      Select All
                    </button>
                    <button className="button-secondary" type="button" onClick={handleClearBenchmarkCases}>
                      Clear
                    </button>
                  </div>
                </div>

                <details className="compact-case-picker">
                  <summary>Choose cases</summary>
                  <div className="case-picker">
                    {cases.map((item) => (
                      <label key={item} className="checkbox-row">
                        <input
                          type="checkbox"
                          checked={selectedBenchmarkCases.includes(item)}
                          onChange={() => handleToggleBenchmarkCase(item)}
                        />
                        {item}
                      </label>
                    ))}
                  </div>
                </details>

                <button
                  className="button-primary"
                  type="submit"
                  disabled={runningBenchmark || selectedBenchmarkCases.length === 0}
                >
                  {runningBenchmark ? "Running benchmark..." : "Run benchmark"}
                </button>
              </div>
            </form>
          </section>

          <section className="grid two-up">
            <div className="panel-stack">
              <div className="panel detail-panel benchmark-control-card">
                <div className="panel-heading">
                  <h2>Current Benchmark Controls</h2>
                  <p>Filter and sort the most recent benchmark run from this session.</p>
                </div>
                <div className="comparison-picker-grid">
                  <label>
                    Family
                    <select value={currentBenchmarkFamilyFilter} onChange={(event) => setCurrentBenchmarkFamilyFilter(event.target.value)}>
                      {currentBenchmarkFamilyOptions.map((option) => (
                        <option key={`current-${option}`} value={option}>
                          {option === "all" ? "All families" : option}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Sort
                    <select value={currentBenchmarkSortMode} onChange={(event) => setCurrentBenchmarkSortMode(event.target.value as BenchmarkSortMode)}>
                      <option value="risk">Highest risk first</option>
                      <option value="name">Case name</option>
                    </select>
                  </label>
                </div>
              </div>
              <BenchmarkSummaryTable
                report={currentBenchmarkDetail}
                familyFilter={currentBenchmarkFamilyFilter}
                sortMode={currentBenchmarkSortMode}
                title="Current Benchmark"
              />
            </div>

            <div className="panel-stack">
              <div className="panel detail-panel benchmark-control-card">
                <div className="panel-heading">
                  <h2>Selected Benchmark Controls</h2>
                  <p>Choose a saved benchmark and refine the view without affecting the current benchmark.</p>
                </div>
                <div className="comparison-picker-grid">
                  <label>
                    Saved benchmark
                    <select
                      value={selectedBenchmarkDetail?.artifact_path ?? ""}
                      onChange={(event) => {
                        const selected = benchmarks.find((item) => item.artifact_path === event.target.value) ?? null;
                        setSelectedBenchmarkDetail(selected);
                      }}
                    >
                      {benchmarks.map((item) => (
                        <option key={`selected-benchmark-${item.artifact_path ?? item.generated_at_utc}`} value={item.artifact_path}>
                          {item.provider} | {item.model_name} | {formatTimestamp(item.generated_at_utc)}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Family
                    <select value={selectedBenchmarkFamilyFilter} onChange={(event) => setSelectedBenchmarkFamilyFilter(event.target.value)}>
                      {selectedBenchmarkFamilyOptions.map((option) => (
                        <option key={option} value={option}>
                          {option === "all" ? "All families" : option}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Sort
                    <select value={selectedBenchmarkSortMode} onChange={(event) => setSelectedBenchmarkSortMode(event.target.value as BenchmarkSortMode)}>
                      <option value="risk">Highest risk first</option>
                      <option value="name">Case name</option>
                    </select>
                  </label>
                </div>
              </div>
              <BenchmarkSummaryTable
                report={selectedBenchmarkDetail}
                familyFilter={selectedBenchmarkFamilyFilter}
                sortMode={selectedBenchmarkSortMode}
                title="Selected Benchmark"
              />
            </div>
          </section>

        </>
      ) : null}

      {activeTab === "artifacts" ? (
        <>
          <section className="grid full-width">
            <div className="panel detail-panel">
              <div className="panel-heading">
                <h2>Run Comparison</h2>
                <p>Compare two saved run artifacts. Select both artifacts here.</p>
              </div>
              <div className="comparison-picker-grid">
                <label>
                  Left artifact
                  <select value={comparisonLeft} onChange={(event) => setComparisonLeft(event.target.value)}>
                    {runs.map((item) => (
                      <option key={`left-${item.artifact_path ?? item.timestamp_utc}`} value={item.artifact_path}>
                        {resultLabel(item)}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Right artifact
                  <select value={comparisonRight} onChange={(event) => setComparisonRight(event.target.value)}>
                    {runs.map((item) => (
                      <option key={`right-${item.artifact_path ?? item.timestamp_utc}`} value={item.artifact_path}>
                        {resultLabel(item)}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            </div>
          </section>

          <section className="grid full-width">
            <ComparisonTable left={leftComparisonRun} right={rightComparisonRun} />
          </section>

          <section className="grid full-width">
            <div className="panel detail-panel">
              <div className="panel-heading">
                <h2>Benchmark Comparison Controls</h2>
                <p>Compare two saved benchmark artifacts.</p>
              </div>
              <div className="comparison-picker-grid">
                <label>
                  Left benchmark
                  <select value={benchmarkComparisonLeft} onChange={(event) => setBenchmarkComparisonLeft(event.target.value)}>
                    {benchmarks.map((item) => (
                      <option key={`benchmark-left-${item.artifact_path ?? item.generated_at_utc}`} value={item.artifact_path}>
                        {item.provider} | {item.model_name} | {formatTimestamp(item.generated_at_utc)}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Right benchmark
                  <select value={benchmarkComparisonRight} onChange={(event) => setBenchmarkComparisonRight(event.target.value)}>
                    {benchmarks.map((item) => (
                      <option key={`benchmark-right-${item.artifact_path ?? item.generated_at_utc}`} value={item.artifact_path}>
                        {item.provider} | {item.model_name} | {formatTimestamp(item.generated_at_utc)}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            </div>
          </section>

          <section className="grid full-width">
            <BenchmarkComparisonTable left={leftComparisonBenchmark} right={rightComparisonBenchmark} />
          </section>

          <section className="grid full-width">
            <ProviderDifferencesPanel currentReport={currentBenchmarkDetail ?? selectedBenchmarkDetail} benchmarks={benchmarks} />
          </section>

        </>
      ) : null}
    </main>
  );
}
