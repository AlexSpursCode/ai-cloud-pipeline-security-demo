from __future__ import annotations

CONTROL_KEYWORDS = {
    "secret_scanning": ["secret scan", "gitleaks", "trufflehog"],
    "sbom_generation": ["sbom", "cyclonedx", "syft"],
    "dependency_scanning": ["dependency scan", "pip-audit", "safety", "osv"],
    "ai_attack_simulation": ["attack simulation", "prompt injection", "red team"],
    "least_privilege_permissions": ["permissions:", "contents: read", "permissions: read"],
}

CONTROL_METADATA = {
    "secret_scanning": {
        "title": "Secret scanning",
        "severity": "high",
        "owasp_llm": ["LLM06: Sensitive Information Disclosure"],
        "cloud": ["IAM least privilege", "Logging and monitoring"],
        "supply_chain": ["SCM credential hygiene"],
    },
    "sbom_generation": {
        "title": "SBOM generation",
        "severity": "medium",
        "owasp_llm": ["LLM05: Supply Chain Vulnerabilities"],
        "cloud": ["Asset inventory"],
        "supply_chain": ["SBOM and provenance"],
    },
    "dependency_scanning": {
        "title": "Dependency scanning",
        "severity": "high",
        "owasp_llm": ["LLM05: Supply Chain Vulnerabilities"],
        "cloud": ["Vulnerability management"],
        "supply_chain": ["Dependency risk monitoring"],
    },
    "ai_attack_simulation": {
        "title": "AI attack simulation",
        "severity": "high",
        "owasp_llm": ["LLM01: Prompt Injection", "LLM07: Insecure Plugin Design"],
        "cloud": ["Continuous validation"],
        "supply_chain": ["Release security testing"],
    },
    "least_privilege_permissions": {
        "title": "Least-privilege permissions",
        "severity": "critical",
        "owasp_llm": ["LLM08: Excessive Agency"],
        "cloud": ["IAM least privilege"],
        "supply_chain": ["Workflow hardening"],
    },
}
