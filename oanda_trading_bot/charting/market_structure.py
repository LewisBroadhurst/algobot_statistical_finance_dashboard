class MarketStructure:

    def __init__(self, df):
        self.df = df
        self.fib_38_retracement_point = 0

        self.uptrend = True
        self.HH = 0
        self.HL = 0.98847
        self.HHs = []
        self.HLs = []
        self.confirmed_HL = 0
        self.HL_to_HH_max_distance = 0

        self.downtrend = False
        self.LL = 1000
        self.LH = 0
        self.LLs = []
        self.LHs = []
        self.confirmed_LH = 1000
        self.LH_to_LL_max_distance = 0


    # Bullish Functions


    def bull_continuation(self, row):
        """Confirms LH and new leg in price."""
        if len(self.HLs) > 0:
            if self.HH < row.mid_c:
                self.HLs.sort()
                self.HL = self.HLs[0]
                self.HLs = []
                self.uptrend = True
                self.confirmed_HL = self.HL
                print(f'BOS. Current Price: {row.mid_c}. Uptrend: {self.uptrend}. Confirmed HH: {self.HH}. '
                      f'Confirmed HL: {self.confirmed_HL}. ID: bull_continuation.')

    def bull_HH_check(self, row):
        if row.mid_c > self.HH:
            self.HH = row.mid_c
            self.HHs.append(self.HH)

    def bull_retracement_check(self, row):
        if row.mid_c < self.fib_38_retracement_point:
            self.HLs.append(row.mid_c)
            self.HLs.sort()
            self.HL = self.HLs[0]

    def bull_reversal_check(self, row):
        if row.mid_c < self.confirmed_HL:
            self.uptrend = False
            self.downtrend = True
            self.LH = self.HH
            self.confirmed_LH = self.HH
            self.LL = row.mid_c
            self.LHs = []
            print(f"REVERSAL. Current price: {row.mid_c}. Downtrend = {self.downtrend}. "
                  f"Uptrend = {self.uptrend}. HL: {self.LH} ID: bull_reversal.")

    def run_bull_ms(self, row):
        # Checking for continuation BOS
        self.bull_continuation(row)

        # Checking for new HH (no BOS)
        self.bull_HH_check(row)

        # Max Dist calculation & Retracement Point calculation
        self.HL_to_HH_max_distance = self.HH - self.HL
        self.fib_38_retracement_point = self.HL + (self.HL_to_HH_max_distance * 0.62)

        # Checking Retracement %
        self.bull_retracement_check(row)

        # Checking for reversal BOS
        self.bull_reversal_check(row)


    # Bearish Functions


    def bear_continuation(self, row):
        if len(self.LHs) > 0:
            if self.LL > row.mid_c:
                self.LHs.sort()
                self.LH = self.LHs[-1]
                self.LHs = []
                self.downtrend = True
                self.confirmed_LH = self.LH
                print(f'BOS. Current Price: {row.mid_c}. Downtrend: {self.downtrend}. Confirmed LL: {self.LL}.'
                      f'Confirmed LH: {self.confirmed_LH}. ID: bear_continuation.')

    def bear_LL_check(self, row):
        if row.mid_c < self.LL:
            self.LL = row.mid_c
            self.LLs.append(self.LL)

    def bear_retracement_check(self, row):
        if row.mid_c > self.fib_38_retracement_point:
            self.LHs.append(row.mid_c)
            self.LHs.sort()
            self.LH = self.LHs[-1]

    def bear_reversal_check(self, row):
        if row.mid_c > self.confirmed_LH:
            self.uptrend = True
            self.downtrend = False
            self.HL = self.LL
            self.confirmed_HL = self.LL
            self.HH = row.mid_c
            self.HLs = []
            print(f"REVERSAL --> Down -> Up. Current price: {row.mid_c}. Downtrend = {self.downtrend}. "
                  f"Uptrend = {self.uptrend}")

    def run_bear_ms(self, row):
        # Checking for continuation BOS
        self.bear_continuation(row)

        # Checking for new LL (no BOS)
        self.bear_LL_check(row)

        # Max Dist calculation & Retracement Point calculation
        self.LH_to_LL_max_distance = self.LH - self.LL
        self.fib_38_retracement_point = self.LL + (self.LH_to_LL_max_distance * 0.38)

        # Checking Retracement %
        self.bull_retracement_check(row)

        # Checking for BOS
        self.bear_reversal_check(row)


    # Run Simulation


    def run_simulation(self):
        for _, row in self.df.iterrows():

            if self.uptrend is True:
                self.run_bull_ms(row)

            if self.downtrend is True:
                self.run_bear_ms(row)