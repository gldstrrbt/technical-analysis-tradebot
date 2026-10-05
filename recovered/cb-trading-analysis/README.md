# Recovered trading & market-analysis experiments

This directory preserves a cleaned selection of Shane Lessa's 2019–2020 trading,
backtesting, exchange-integration, and market-analysis experiments recovered from
an old working directory labelled `cb`.

It is intentionally an **archive**, not a current trading system. The scripts
span Coinbase/Coinbase Pro, Binance, Robinhood, Cobinhood, crypto market-cap
analysis, backtesting, RSI/SMA strategy experiments, Selenium/browser automation,
and live/dry-run prototypes.

## Cleanup performed

- Exact duplicate files and obvious backup copies were omitted.
- Vendored third-party libraries and cloned packages were omitted.
- CSV market dumps, logs, browser binaries, caches, build output, and nested
  source archives were omitted.
- Credential files, API tokens, account identifiers, email app passwords, OAuth
  client credentials, and wallet recovery material were excluded or replaced by
  environment-variable lookups/placeholders.
- Extremely large inline historical test datasets embedded in a few scripts were
  removed while preserving the surrounding code.
- Versioned files were retained only when they represented materially different
  experiments rather than byte-for-byte copies.

These files are preserved as historical development work and may rely on APIs,
packages, or endpoints that have changed since they were written.

## Additional recovery batch

A later `cb` folder pass added distinct historical variants and utilities for ATH tracking, CoinGecko/market-cap analysis, Robinhood RSI testing, yield-curve work, crypto news crawling, and additional Binance/Coinbase experiments. Exact duplicates and obvious backup snapshots were omitted; generated datasets and credential-only files were not committed. See [`BATCH_NOTES.md`](./BATCH_NOTES.md).
