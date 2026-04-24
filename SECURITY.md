# Security Policy

## Purpose

Invariant is a security-related open source project.

This document explains how to report suspected vulnerabilities or sensitive
security issues.

## Reporting a Vulnerability

Please do **not** report sensitive security issues in a public GitHub issue.

Instead, report them privately to:

- `security@echoforgex.com`

Include:
- a clear description of the issue
- affected component or workflow
- reproduction steps if available
- impact assessment if known
- any relevant logs, screenshots, or artifact names

## What To Report Privately

Use private disclosure for issues such as:
- vulnerabilities in provider integrations
- weaknesses in scenario or artifact handling that expose secrets
- vulnerabilities in the UI/API that could affect users or operator data
- any issue that could reasonably be exploited before a fix is available

## What Can Go In Public Issues

Public issues are appropriate for:
- non-sensitive bugs
- documentation errors
- UX problems
- feature requests
- benchmark or evaluator quality issues that are not themselves sensitive

## Response Expectations

The project will attempt to:
- acknowledge receipt
- assess severity and reproducibility
- determine whether the issue should remain private during remediation

Response times are best-effort and should not be interpreted as a contractual
support commitment.

## Scope

This policy applies to:
- the open source repository
- the harness
- the UI
- the benchmark and custom testing workflows

## License and Branding

Security reporting does not change the terms of the Apache-2.0 license or any
EchoForgeX branding terms. Those remain governed by the repository license and
project documentation.
