# Final cb folder recovery batch

This batch preserves the remaining distinct authored experiments from the old `cb` working directory.

Included:
- a later `bn_00` Binance trading/data snapshot
- several distinct Turtle-strategy iterations and a backtest variant
- stock/FTSE loss and signal-analysis experiments
- a PredictIt market-chart collector/plotter
- a small compounding scratch calculator

Cleanup performed:
- replaced embedded Binance API credentials with environment variables
- omitted `new_history.py` because it is byte-for-byte identical to the copy already archived
- omitted `six.py` and `easy_install.py` because they are third-party package files
- omitted `binance.py` because it is a vendored third-party Binance client implementation, not project-specific source
- omitted `bloom.json` because it is a market-data snapshot rather than source code
- trimmed a large commented numeric dump from the calculator scratch file

These are historical experiments. Some depend on APIs, libraries, endpoints, or data files that have changed or disappeared.