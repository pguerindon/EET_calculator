---
title: EEP Integration Guide
subtitle: Integration Specification
date: August 2026
toc: true
numbersections: true
geometry:
  - left=2cm
  - right=2cm
  - top=1cm
  - bottom=1cm
---

| Field | Value |
|-------|-------|
| Version | 1.1 |
| Status | Official Release |
| Publication Date | August 2026 |

\newpage

# EEP Integration Guide

## Revision History

| Version | Date | Description |
|:--------|:-----|:------------|
| 1.1 | 2026 | Added synchronization workflow, direct calculation recall, server version reporting and integration recommendations. |
| 1.0 | 2026 | Initial public release. |

## Introduction

### Purpose

This guide explains how to integrate a Timing System with the EET Calculator using the Electronic Equivalent Time Exchange Protocol (EEP).

### Scope

This guide describes:

- EET Calculator architecture;
- Calculation Model;
- Initial Request;
- Optional Secondary Request;
- EEP Endpoints;
- Integration Recommendations.
- Calculation synchronization;
- Direct calculation recall;
- Server version reporting.

Request and response bodies are defined in the EEP Specification.

### Related Documents

- EEP Specification
- EET Calculator Administrator Guide


# System Overview

An Initial Request creates a Calculation Document from the supplied Electronic Times (ET) and returns a unique Calculation Key.

Optional Secondary Requests enrich the same Calculation Document by providing Manual Times (MT) using its Calculation Key.

The Calculation Document is then available in the web interface using its Calculation Key.

```{=latex}
\newpage
```

![](../images/system_overview.png){ width=80% }

# Calculation Model

The EET Calculator manages each calculation as a Calculation Document identified by a unique Calculation Key.

A Calculation Document:

- is created by an Initial Request;
- may be enriched by Optional Secondary Requests;
- is then processed through the web interface.

The Calculation Key uniquely identifies the Calculation Document throughout its lifetime.

## Calculation Document

The Calculation Document is the persistent representation of an EET calculation.

It contains all information required for calculation and reporting.

It may be progressively enriched by Optional Secondary Requests before calculation.

## Calculation Key

It is assigned when the Calculation Document is created.

The same Calculation Key shall be used in all subsequent requests related to that Calculation Document.

## Calculation Lifecycle

1. Creation by an Initial Request.
2. Optional enrichment by one or more Secondary Requests.
3. Optional synchronization with the server.
4. Completion and calculation through the web interface.

Calculation Documents may subsequently be deleted by an explicit DELETE request or automatically according to the server retention policy.

![](../images/calculation_document_lifecycle.png){ width=90% }

# Initial Request

## Purpose

Creates a new Calculation Document from the supplied Electronic Times (ET).

## Processing

Upon successful validation, the server creates and persists a new Calculation Document.

## Multiple Requests

Each request is independent. Repeating the same request creates a new Calculation Document with a different Calculation Key.

# Optional Secondary Request

## Purpose

Enriches an existing Calculation Document by providing Manual Times (MT).

## Processing

Upon successful validation, updates and persists the Calculation Document identified by its Calculation Key.

## Multiple Requests

Each request updates the same Calculation Document. Previously supplied Manual Times are replaced by the new values.

# Calculation Synchronization

Timing software may periodically synchronize its locally stored Calculation Keys with the EET Calculator server.

The client submits a list of Calculation Keys.

For each key, the server reports:

- whether the calculation still exists;
- its processing mode.

This allows client software to remove expired TEST calculations while preserving valid calculations.

# Direct Calculation Recall

A Calculation Document may be recalled directly through its Calculation Key.

This mechanism allows:

- review of an existing calculation;
- manual completion of missing Manual Times;
- PDF generation;
- further processing by the Technical Delegate.

The recalled Calculation Key remains visible in the user interface.

# EEP Endpoints

| Endpoint | HTTP Method | Purpose |
|----------|:-----------:|---------|
| Initial Request | POST | Creates a Calculation Document |
| Optional Secondary Request | POST | Enriches a Calculation Document |
| Calculation Synchronization | POST | Verifies Calculation Keys |
| Calculation Recall | GET | Opens a Calculation Document |

Request and response bodies are defined in the EEP Specification.

Every successful EEP request returns the associated Calculation Key.

Error responses are defined in the EEP Specification.

Calculation Synchronization returns, for each supplied Calculation Key:

- existence;
- processing mode.

Calculation Recall opens the corresponding Calculation Document in the web interface.

# Server Version Reporting

Every successful EEP response includes informational messages indicating:

- the implemented EEP protocol version;
- the implemented EET Calculator version.

These messages are intended for diagnostic purposes and allow client software to verify compatibility with the server implementation.

Client software should treat these messages as informational only.

# Integration Recommendations

- Preserve the Calculation Key for the lifetime of the Calculation Document.
- Avoid duplicate Initial Requests.
- Periodically synchronize locally stored Calculation Keys.
- Use server version information to detect implementation differences.
- Ignore informational server messages not required by the application.