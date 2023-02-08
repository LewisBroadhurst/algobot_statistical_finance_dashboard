import pandas as pd

OB = 80
ENGULFING_FACTOR = 1.2


def apply_ob(row):
    if row.body_perc >= 75:
        return True
    return False


def apply_engulfing(row):
    if row.direction != row.direction_prev:
        if row.body_size > row.body_size_prev * ENGULFING_FACTOR:
            return True
    return False


def apply_engulfing_obs(row):
    if row.direction != row.direction_prev \
            and row.prev_OB is True\
            and row.body_perc > 0.5\
            and row.body_size > 0.00015 < row.body_size_prev \
            and row.body_size > row.body_size_prev * ENGULFING_FACTOR:
        return True
    return False


def apply_candle_props(df: pd.DataFrame):
    df_an = df.copy()
    direction = df_an.mid_c - df_an.mid_o
    body_size = abs(direction)
    direction = [1 if x >= 0 else -1 for x in direction]
    full_range = df_an.mid_h - df_an.mid_l
    body_perc = (body_size / full_range) * 100

    df_an['body_size'] = body_size
    df_an['body_size_prev'] = df_an.body_size.shift(1)
    # df_an['body_size_prev_2'] = df_an.body_size.shift(2)

    df_an['direction'] = direction
    df_an['direction_prev'] = df_an.direction.shift(1)
    # df_an['direction_prev_2'] = df_an.direction.shift(2)

    df_an['body_perc'] = body_perc
    df_an['body_perc_prev'] = df_an.body_perc.shift(1)
    # df_an['body_perc_prev_2'] = df_an.body_perc.shift(2)

    df_an['OB'] = df_an.apply(apply_ob, axis=1)
    df_an['prev_OB'] = df_an['OB'].shift(1)
    # df_an['prev_OB_2'] = df_an['OB'].shift(2)

    df_an['ENGULFING_OB'] = df_an.apply(apply_engulfing_obs, axis=1)

    return df_an
