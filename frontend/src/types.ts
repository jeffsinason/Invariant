export type ProviderInfo = {
  provider: string;
  default_model: string;
};

export type ModelInfo = {
  provider: string;
  id: string;
  display_name: string;
  recommended_default: boolean;
  recommended_for_harness: boolean;
  source?: string;
};

export type ToolCall = {
  name: string;
  arguments: Record<string, unknown>;
};

export type UsagePayload = Record<string, unknown> | null;

export type CaseResultArtifact = {
  artifact_path?: string;
  saved_path?: string | null;
  case_name: string;
  provider: string;
  model_name: string;
  vulnerable: boolean;
  evaluation_label?: string | null;
  response_text: string;
  notes: string;
  request_id?: string | null;
  stop_reason?: string | null;
  usage?: UsagePayload;
  tool_calls?: ToolCall[] | null;
  timestamp_utc: string;
  error_type?: string | null;
  error_message?: string | null;
  raw_response?: unknown;
};

export type CaseRunResponse = {
  result: CaseResultArtifact;
};

export type BenchmarkSummary = {
  total_cases: number;
  vulnerable_cases: number;
  safe_cases: number;
};

export type BenchmarkResultRow = {
  case_name: string;
  provider: string;
  model_name: string;
  vulnerable: boolean;
  evaluation_label?: string | null;
  response_text: string;
  request_id?: string | null;
  stop_reason?: string | null;
  usage?: UsagePayload;
  tool_call_count: number;
  tool_call_names: string[];
  timestamp_utc: string;
};

export type BenchmarkArtifact = {
  artifact_path?: string;
  report_type: string;
  provider: string;
  model_name: string;
  generated_at_utc: string;
  summary: BenchmarkSummary;
  results: BenchmarkResultRow[];
};

export type BenchmarkRunResponse = {
  report: BenchmarkArtifact;
  saved_case_paths: string[];
  saved_report_path?: string | null;
};
