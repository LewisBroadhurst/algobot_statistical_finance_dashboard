class DailyHighsLows:

    def __init__(self, m5_df):
        self.df = m5_df.copy()
        self.pdhs = []
        self.pdls = []

    def refresh_hods_lods(self, row, df):

        if row.time.hour == 22 and row.time.minute == 0 and (row.name - 288) > 0:

            start_of_pd = row.name - 288
            end_of_pd = row.name

            df_hod = df.iloc[start_of_pd:end_of_pd].copy()
            hod = df_hod.mid_h.max()

            df_lod = df.iloc[start_of_pd:end_of_pd].copy()
            lod = df_lod.mid_h.max()

            if len(self.pdhs) == 3:
                self.pdhs.pop()
            if len(self.pdls) == 3:
                self.pdls.pop()

            self.pdhs.append(hod)
            self.pdls.append(lod)

    # TODO: How to remove price effectively after HOD/LOD is taken?
        # => Period of time?
        # => If trade is taken?
        # => Quite hard to do effectively.