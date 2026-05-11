# MCP Kaggle Integration

## Status

No official Kaggle MCP confirmed. Using Kaggle CLI (`kaggle` Python package) via wrapper scripts.

## Safe Operations (Read-Only)

```bash
kaggle competitions list -s "orbit wars"
kaggle competitions files orbit-wars
kaggle competitions submissions orbit-wars
```

These are safe to run at any time.

## Operations Requiring Human Confirmation

```bash
# Download competition data
kaggle competitions download orbit-wars -p data/raw

# Submit — always via wrapper script
python scripts/submit_kaggle.py \
  --file submission/submission.tar.gz \
  --message "expXXX description" \
  --no-dry-run \
  --confirm "CONFIRMO SUBIR A KAGGLE"
```

## Authentication

Place `kaggle.json` in `~/.kaggle/kaggle.json` with `chmod 600`.
Never commit `kaggle.json` to the repository.

## MCP Server (If Used)

If a community Kaggle MCP server is adopted:
- Audit the server code before use.
- Use read-only tools only until fully reviewed.
- Never expose submit tool to the LLM without human-in-the-loop confirmation.
- Fix the MCP server version.
- Log all MCP tool calls.
- Do not pass `kaggle.json` contents to the model context.
