# Demo flow

1. Show `pipelines/vulnerable-github-actions.yml` to establish an insecure starting point.
2. Run the risk mapper and highlight missing controls and mapped frameworks.
3. Launch the app in `APP_MODE=vulnerable` and run the attack simulator.
4. Show that prompt injection and synthetic secret disclosure succeed.
5. Switch the app to `APP_MODE=hardened`.
6. Re-run the attack simulator and show the attacks being blocked.
7. Finish with `scripts/generate_report.sh` as the final release gate.
