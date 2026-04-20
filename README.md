# Red Team Fuzzing Payloads (2026 Edition)

`✅[STATUS: ACTIVE / CONTINUOUSLY UPDATED]`

## 📜 Overview
This repository contains a highly curated, 2026-optimized collection of discovery payloads, wordlists, and fuzzing dictionaries. Designed for offensive security operations (Red Teaming) and automated Attack Surface Management (ASM), these assets are used to identify hidden endpoints, misconfigurations, and vulnerabilities across modern cloud-native and AI-driven infrastructures.

As a Senior Site Reliability & Security Engineer, I maintain this living repository to ensure my offensive toolset evolves alongside the defensive architectures I build. 

## 🎯 Target Vectors & 2026 Threat Landscape
The payloads in this repository are structured to target the most critical attack surfaces in today's distributed systems:

* 🧠 **AI Infrastructure & LLM Ops:** Specialized payloads for testing AI Gateways, executing Prompt Injection scenarios, and auditing RAG (Retrieval-Augmented Generation) pipelines for data leakage.
* 🌐 **API & Microservices:** Fuzzing dictionaries targeting GraphQL introspection, gRPC endpoints, and undocumented REST API versions.
* ☁️ **Cloud Identity & IAM:** Assets for discovering exposed JWT tokens, misconfigured cloud metadata endpoints (AWS IMDSv2, GCP Metadata), and Zero Trust policy bypasses.
* 🏗️ **CI/CD & Supply Chain:** Payloads aimed at identifying exposed `.git` directories, `.env` files, and vulnerable CI/CD pipeline configurations within staging environments.

## 📦 Asset Index

The repository is structured into specialized directories, each targeting a specific vector of the modern attack surface:

### 🌐 Web & Infrastructure (`/web_fuzzing/`)
* `web_ext_common.txt`: A baseline, high-speed fuzzing list optimized for modern web server extensions, hidden directories, and exposed configuration files (e.g., `.env`, `.kube/config`). Used extensively with tools like `ffuf` and `feroxbuster`.

### 🧠 AI Infrastructure & LLM Ops (`/ai_llm_fuzzing/`)
* `prompt_injections.txt`: Modern LLM jailbreaks, system prompt extraction strings, and context window bypasses designed to test AI Gateway guardrails.
* `rag_poisoning.txt`: Payloads crafted for Vector Database manipulation, semantic hijacking, and testing Retrieval-Augmented Generation architectures.

### 🔌 API & Microservices (`/api_microservices/`)
* `graphql_discovery.txt`: Dictionaries containing introspection queries, batching attack payloads, and common unauthorized mutation endpoints.
* `grpc_endpoints.txt`: Reflection targets and internal microservice port definitions used to map out backend service meshes.

### ☁️ Cloud Identity & Zero Trust (`/cloud_identity/`)
* `jwt_bypasses.txt`: Payloads for testing API Gateways against algorithmic confusion (e.g., `alg: none`), signature stripping, and malformed claim structures.
* `metadata_ssrf.txt`: High-value targets for Server-Side Request Forgery, focusing on AWS IMDSv2, GCP Metadata, Azure instance identities, and internal Kubernetes endpoints.

### 🏗️ CI/CD & Supply Chain (`/cicd_supply_chain/`)
* `exposed_configs.txt`: Paths aimed at detecting orphaned infrastructure state files (e.g., `terraform.tfstate`), pipeline definitions (`.gitlab-ci.yml`), and configuration leaks in staging environments.

### 🛠️ Automation & Tooling (`/scripts/`)
* `asm_fuzz_runner.py`: A production-grade, asynchronous Python fuzzer (using `aiohttp`). Designed for seamless integration into CI/CD pipelines to provide automated, continuous Attack Surface Management validation.


## 🛡️ The Defensive Perspective (SRE Context)
"To build impenetrable systems, you must know how to break them." 

Integrating these offensive assets into CI/CD pipelines allows for continuous, automated security validation. By fuzzing our own infrastructure before deployment, we shift security left, transforming reactive patching into proactive architecture hardening.

---
*Disclaimer: All payloads and scripts in this repository are for educational purposes, authorized auditing, and defensive engineering only. Always ensure you have explicit permission before scanning or testing any infrastructure.*
