import pandas as pd

OB = 80
ENGULFING_FACTOR = 1.1


def apply_ob(row):
    if row.body_perc > OB:
        return True

    return False


def apply_engulfing(row):
    if row.direction != row.direction_prev:
        if row.body_size > row.body_size_prev * ENGULFING_FACTOR:
            return True
    return False


def apply_engulfing_ob(row):
    if row.direction != row.direction_prev:
        if row.body_size > row.body_size_prev * ENGULFING_FACTOR:
            return True
    return False


def apply_candle_props(df: pd.DataFrame):

    df_an = df.copy()
    direction = df_an.mid_c - df_an.mid_o
    body_size = abs(direction)
    direction = [1 if x >= 0 else -1 for x in direction]
    full_range = df_an.mid_h - df_an.mid_l
    body_perc = (body_size / full_range) * 100

    df_an['body_perc'] = body_perc
    df_an['direction'] = direction
    df_an['body_size'] = body_size
    df_an['body_size_prev'] = df_an.body_size.shift(1)
    df_an['direction_prev'] = df_an.direction.shift(1)
    df_an['body_perc_prev'] = df_an.body_perc.shift(1)

    return df_an


def set_candle_patterns(df_an: pd.DataFrame):
    df_an['ENGULFING'] = df_an.apply(apply_engulfing, axis=1)
    df_an['OB'] = df_an.apply(apply_ob, axis=1)


def apply_patterns(df: pd.DataFrame):
    df_an = apply_candle_props(df)
    set_candle_patterns(df_an)
    return df_an