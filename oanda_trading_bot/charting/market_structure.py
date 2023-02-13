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


    def run_simulation(self):
        for _, row in self.df.iterrows():

            if self.uptrend is True:

                # Checking for continuation BOS
                if len(self.HLs) > 0:
                    if self.HH < row.mid_c:
                        self.HLs.sort()
                        self.HL = self.HLs[0]
                        self.HLs = []
                        self.uptrend = True
                        self.confirmed_HL = self.HL
                        print(f'BOS. Current Price: {row.mid_c}. Uptrend: {self.uptrend}. Confirmed HH: {self.HH}. '
                              f'Confirmed HL: {self.confirmed_HL}. ID: 3')

                # Checking for new HH (no BOS)
                if row.mid_c > self.HH:
                    self.HH = row.mid_c
                    self.HHs.append(self.HH)

                # Max Dist calculation & Retracement Point calculation
                self.HL_to_HH_max_distance = self.HH - self.HL
                self.fib_38_retracement_point = self.HL + (self.HL_to_HH_max_distance * 0.62)

                # Checking Retracement %
                if row.mid_c < self.fib_38_retracement_point:
                    self.HLs.append(row.mid_c)
                    self.HLs.sort()
                    self.HL = self.HLs[0]


                # Checking for reversal BOS
                if row.mid_c < self.confirmed_HL:
                    print(self.confirmed_HL)
                    self.uptrend = False
                    self.downtrend = True
                    self.LH = self.HH
                    self.confirmed_LH = self.HH
                    self.LL = row.mid_c
                    self.LHs = []
                    print(f"REVERSAL. Current price: {row.mid_c}. Downtrend = {self.downtrend}. "
                          f"Uptrend = {self.uptrend}. HL: {self.LH} ID:1.")


            if self.downtrend is True:

                # Checking for continuation BOS
                if len(self.LHs) > 0:
                    if self.LL > row.mid_c:
                        self.LHs.sort()
                        self.LH = self.LHs[-1]
                        self.LHs = []
                        self.downtrend = True
                        self.confirmed_LH = self.LH
                        print(f'BOS. Current Price: {row.mid_c}. Downtrend: {self.downtrend}. Confirmed LL: {self.LL}.'
                              f'Confirmed LH: {self.confirmed_LH}. ID:2.')

                # Checking for new LL (no BOS)
                if row.mid_c < self.LL:
                    self.LL = row.mid_c
                    self.LLs.append(self.LL)

                # Max Dist calculation & Retracement Point calculation
                self.LH_to_LL_max_distance = self.LH - self.LL
                self.fib_38_retracement_point = self.LL + (self.LH_to_LL_max_distance * 0.38)

                # Checking Retracement %
                if row.mid_c > self.fib_38_retracement_point:
                    self.LHs.append(row.mid_c)
                    self.LHs.sort()
                    self.LH = self.LHs[-1]

                # Checking for BOS
                if row.mid_c > self.confirmed_LH:
                    self.uptrend = True
                    self.downtrend = False
                    self.HL = self.LL
                    self.confirmed_HL = self.LL
                    self.HH = row.mid_c
                    self.HLs = []
                    print(f"REVERSAL --> Down -> Up. Current price: {row.mid_c}. Downtrend = {self.downtrend}. "
                          f"Uptrend = {self.uptrend}")