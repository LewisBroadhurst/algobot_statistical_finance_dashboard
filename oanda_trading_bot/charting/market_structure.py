class MarketStructure:

    def __init__(self, df):
        self.df = df

        self.uptrend = True
        self.HH = 0
        self.HL = 0.98847
        self.HHs = []
        self.HLs = []
        self.confirmed_HL = 0

        self.downtrend = False
        self.LL = 1000
        self.LH = 0
        self.LLs = []
        self.LHs = []
        self.confirmed_LH = 1000

    def bos_continuation_bull(self, row):
        if len(self.HLs) > 0:
            if self.HH < row.mid_c:
                self.HLs.sort()
                self.HL = self.HLs[0]
                self.HLs = []
                self.uptrend = True
                self.confirmed_HL = self.HL
                print(f'BOS. Current Price: {row.mid_c}. Uptrend: {self.uptrend}. Confirmed HH: {self.HH}. '
                      f'Confirmed HL: {self.confirmed_HL}. ID: bull_continuation.')

    def new_HH(self, row):
        if row.mid_c > self.HH:
            self.HH = row.mid_c
            self.HHs.append(self.HH)

    def retracement_check_bull(self, row):
        # Max Dist calculation
        HL_to_HH_max_distance = self.HH - self.HL
        # Retracement Point calculation
        fib_38_retracement_point = self.HL + (HL_to_HH_max_distance * 0.62)

        # Checking Retracement %
        if row.mid_c < fib_38_retracement_point:
            self.HLs.append(row.mid_c)
            self.HLs.sort()
            self.HL = self.HLs[0]

    def reversal_check_bull(self, row):
        if row.mid_c < self.confirmed_HL:
            print(self.confirmed_HL)
            self.uptrend = False
            self.downtrend = True
            self.LH = self.HH
            self.confirmed_LH = self.HH
            self.LL = row.mid_c
            self.LHs = []
            print(f"REVERSAL. Current price: {row.mid_c}. Downtrend = {self.downtrend}. "
                  f"Uptrend = {self.uptrend}. HL: {self.LH} ID: bull_reversal.")

    def bos_continuation_bear(self, row):
        if len(self.LHs) > 0:
            if self.LL > row.mid_c:
                self.LHs.sort()
                self.LH = self.LHs[-1]
                self.LHs = []
                self.downtrend = True
                self.confirmed_LH = self.LH
                print(f'BOS. Current Price: {row.mid_c}. Downtrend: {self.downtrend}. Confirmed LL: {self.LL}.'
                      f'Confirmed LH: {self.confirmed_LH}. ID: bear_continuation.')

    def new_LL(self, row):
        if row.mid_c < self.LL:
            self.LL = row.mid_c
            self.LLs.append(self.LL)

    def retracement_checker_bear(self, row):
        # Max Dist calculation
        LH_to_LL_max_distance = self.LH - self.LL
        # Retracement Point calculation
        fib_38_retracement_point = self.LL + (LH_to_LL_max_distance * 0.38)

        # Checking Retracement %
        if row.mid_c > fib_38_retracement_point:
            self.LHs.append(row.mid_c)
            self.LHs.sort()
            self.LH = self.LHs[-1]

    def reversal_checker_bear(self, row):
        if row.mid_c > self.confirmed_LH:
            self.uptrend = True
            self.downtrend = False
            self.HL = self.LL
            self.confirmed_HL = self.LL
            self.HH = row.mid_c
            self.HLs = []
            print(f"REVERSAL --> Down -> Up. Current price: {row.mid_c}. Downtrend = {self.downtrend}. "
                  f"Uptrend = {self.uptrend}")

    def run_uptrend_downtrend_func(self, row):
        if self.uptrend is True:
            # Checking for continuation BOS
            self.bos_continuation_bull(row)
            # Checking for new HH (no BOS)
            self.new_HH(row)
            # Checking for retracement
            self.retracement_check_bull(row)
            # Checking for reversal BOS
            self.reversal_check_bull(row)
        else:
            # Checking for continuation BOS
            self.bos_continuation_bear(row)
            # Checking for new LL (no BOS)
            self.new_LL(row)
            # Checking Retracement %
            self.retracement_checker_bear(row)
            # Checking for BOS
            self.reversal_checker_bear(row)

    def run_simulation(self):

        for _, row in self.df.iterrows():
            self.run_uptrend_downtrend_func(row)