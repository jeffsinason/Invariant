import type {
  BenchmarkArtifact,
  BenchmarkRunResponse,
  CaseResultArtifact,
  CaseRunResponse,
  ModelInfo,
  ProviderInfo,
} from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const message =
      typeof errorBody?.detail?.error_message === "string"
        ? errorBody.detail.error_message
        : `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

export function fetchProviders(): Promise<ProviderInfo[]> {
  return request<ProviderInfo[]>("/providers");
}

export function fetchModels(provider?: string): Promise<ModelInfo[]> {
  const path = provider ? `/models?provider=${encodeURIComponent(provider)}` : "/models";
  return request<ModelInfo[]>(path);
}

export function fetchCases(): Promise<string[]> {
  return request<string[]>("/cases");
}

export function fetchRuns(): Promise<CaseResultArtifact[]> {
  return request<CaseResultArtifact[]>("/runs");
}

export function fetchBenchmarks(): Promise<BenchmarkArtifact[]> {
  return request<BenchmarkArtifact[]>("/benchmarks");
}

export function runCase(input: {
  case_name: string;
  provider: string;
  model_name: string;
  save: boolean;
}): Promise<CaseRunResponse> {
  return request<CaseRunResponse>("/runs/case", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function runBenchmark(input: {
  provider: string;
  model_name: string;
  case_names: string[];
  save: boolean;
}): Promise<BenchmarkRunResponse> {
  return request<BenchmarkRunResponse>("/runs/benchmark", {
    method: "POST",
    body: JSON.stringify(input),
  });
}
