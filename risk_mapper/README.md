# Risk mapper

`risk_mapper` parses CI/CD YAML from `pipelines/`, checks for missing controls, maps the gaps to multiple frameworks, and writes reports to `reports/generated/`.

Controls checked:

- secret scanning
- SBOM generation
- dependency scanning
- AI attack simulation
- least-privilege permissions

Outputs:

- machine-readable JSON report
- presentation-friendly Markdown summary

Note: `vulnerable-*` pipeline files are treated as demo reference inputs by default. They are reported, but not enforced in the aggregate gate unless `RISK_MAPPER_INCLUDE_VULNERABLE=true`.
