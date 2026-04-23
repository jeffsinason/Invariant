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

export type CustomScenarioSummary = {
  scenario_id: string;
  name: string;
  attack_family: string;
  mode: "exploratory" | "evaluated";
  updated_at: string;
  tags: string[];
  artifact_path?: string;
};

export type CustomScenario = {
  schema_version: string;
  scenario_id: string;
  name: string;
  description: string;
  mode: "exploratory" | "evaluated";
  authoring_mode: "guided" | "advanced";
  attack_family: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  target_config: {
    default_provider?: string | null;
    default_model?: string | null;
    targets: Array<{
      provider: string;
      model: string;
      parameters: Record<string, unknown>;
    }>;
  };
  context: {
    trusted: {
      system_instructions: string;
      developer_instructions?: string | null;
      output_constraints: string[];
      tool_policy: Record<string, unknown>;
    };
    user: {
      current_request: string;
      conversation_turns: Array<{ role: string; content: string }>;
    };
    untrusted: {
      retrieved_documents: Array<{
        document_id?: string | null;
        title: string;
        content_type: string;
        content: string;
        metadata: Record<string, unknown>;
      }>;
      tool_outputs: Array<{
        tool_name: string;
        content: string;
        content_type: string;
      }>;
      notes: string[];
    };
    memory: {
      session_summary?: string | null;
      memory_items: Array<{
        memory_id?: string | null;
        content: string;
        source: string;
        trust_level: string;
      }>;
    };
    tools: {
      available_tools: Array<{
        name: string;
        description: string;
        parameters_schema: Record<string, unknown>;
        authorization: Record<string, unknown>;
      }>;
    };
  };
  attack: {
    family: string;
    template?: string | null;
    placement: string;
    timing: string;
    payload: string;
    objective?: string | null;
    variants: Array<{
      variant_id?: string | null;
      label: string;
      payload_override?: string | null;
      placement_override?: string | null;
      timing_override?: string | null;
    }>;
  };
  expected_outcome?: {
    required: boolean;
    behavior_category?: string | null;
    forbidden_outputs: string[];
    required_outputs: string[];
    acceptable_labels: string[];
    unacceptable_labels: string[];
  } | null;
  evaluator: {
    type: "builtin" | "configured" | "custom";
    builtin_name?: string | null;
    configured_rules: Record<string, unknown>;
    custom_logic: Record<string, unknown>;
  };
  save_preferences: {
    save_scenario_by_default: boolean;
    save_run_by_default: boolean;
  };
};

export type CustomScenarioResponse = {
  scenario: CustomScenario;
  validation_warnings?: string[];
  saved_path?: string;
};

export type CustomValidationResponse = {
  valid: boolean;
  scenario: CustomScenario;
  validation_warnings: string[];
};

export type CustomRunArtifact = {
  artifact_path?: string;
  artifact_type: "custom_scenario_run";
  scenario_id: string;
  scenario_name: string;
  scenario_mode: "exploratory" | "evaluated";
  attack_family: string;
  provider: string;
  model_name: string;
  variant_id?: string | null;
  verdict: "safe" | "vulnerable" | "error";
  vulnerable: boolean;
  evaluation_label?: string | null;
  reason_summary: string;
  response_text: string;
  request_id?: string | null;
  stop_reason?: string | null;
  usage?: UsagePayload;
  tool_calls?: ToolCall[] | null;
  raw_response?: unknown;
  expected_outcome?: unknown;
  evaluator_snapshot?: unknown;
  scenario_snapshot?: unknown;
  timestamp_utc: string;
  validation_warnings?: string[];
  saved_path?: string;
};

export type CustomRunGroupArtifact = {
  artifact_path?: string;
  artifact_type: "custom_scenario_run_group";
  scenario_id: string;
  scenario_name: string;
  scenario_slug: string;
  scenario_mode: "exploratory" | "evaluated";
  attack_family: string;
  generated_at_utc: string;
  summary: {
    total_runs: number;
    vulnerable_runs: number;
    safe_runs: number;
  };
  validation_warnings?: string[];
  runs: CustomRunArtifact[];
  scenario_snapshot: unknown;
  saved_path?: string;
};

export type CustomRunResponse = {
  result: CustomRunArtifact | CustomRunGroupArtifact;
};
