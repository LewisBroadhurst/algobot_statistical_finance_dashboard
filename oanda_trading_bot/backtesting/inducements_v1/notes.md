# Beating the inducement algo
- Get a set of daily highs
  - Need a time stamp so I can refer to them in future
  - Also need time so I can say when they are taken

- itterows is like how price will move through newly produced candles

- At the end of each day, take a subsample of the last 288 (5m) candles. That is the new High/Low
- Only keep last 7 days of candles.

- ITERROWS ITERROWS ITERROWS

## Plan...
- [ ] Look at last 7 days of PA
- [ ] Generate the daily lows/highs
- [ ] Method that will remove lows/highs that are taken outside of trading window or taken in trading window
- [ ] Enter 'trading mode' within 7:30-4:30 daily
- [ ] If low/high taken, buy/sell of full vol candle
- [ ] TP at xyz / SL at abc