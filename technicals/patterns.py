import pandas as pd

HANGING_MAN_BODY_MAX = 35
HANGING_MAN_HEIGHT = 40
SHOOTING_STAR_BODY_MAX = 65
SHOOTING_STAR_HEIGHT = 40
ENGULFING_FACTOR = 1.001


def apply_hanging_man(row):
    if row.body_bottom_percentage > HANGING_MAN_HEIGHT:
        if row.body_percentage < HANGING_MAN_BODY_MAX:
            return True


def apply_shooting_star(row):
    if row.body_upper_percentage < SHOOTING_STAR_HEIGHT:
        if row.body_percentage < SHOOTING_STAR_BODY_MAX:
            return True
        

def apply_engulfing(row):
    if row.direction != row.direction_previous:
        if row.body_size > (row.body_size_previous * 1.1):
            if row.full_range > row.full_range_previous:
                return True
    
    return False


def apply_candle_properties(df: pd.DataFrame):
    df_analysis = df.copy()

    direction = df_analysis.mid_c - df_analysis.mid_o
    body_size = abs(direction)
    direction = [1 if x >= 0 else -1 for x in direction]
    full_range = df_analysis.mid_h - df_analysis.mid_l
    body_percentage = (body_size / full_range) * 100
    body_lower = df_analysis[['mid_c', 'mid_o']].min(axis = 1)
    body_upper = df_analysis[['mid_c', 'mid_o']].max(axis = 1)
    body_bottom_pecentage = ((body_lower - df_analysis.mid_l) / full_range) * 100
    body_upper_pecentage = ((body_upper - df_analysis.mid_l) / full_range) * 100

    df_analysis['body_lower'] = body_lower
    df_analysis['body_upper'] = body_upper
    df_analysis['body_bottom_percentage'] = body_bottom_pecentage
    df_analysis['body_upper_percentage'] = body_upper_pecentage
    df_analysis['body_percentage'] = body_percentage
    df_analysis['direction'] = direction
    df_analysis['body_size'] = body_size
    df_analysis['full_range'] = full_range
    df_analysis['body_size_previous'] = df_analysis.body_size.shift(1)
    df_analysis['direction_previous'] = df_analysis.direction.shift(1)
    df_analysis['full_range_previous'] = df_analysis.full_range.shift(1)

    return df_analysis


def set_candle_patterns(df_analysis: pd.DataFrame):
    df_analysis['HANGING_MAN'] = df_analysis.apply(apply_hanging_man, axis = 1)
    df_analysis['SHOOTING_STAR'] = df_analysis.apply(apply_shooting_star, axis = 1)
    df_analysis['ENGULFING'] = df_analysis.apply(apply_engulfing, axis = 1)


def apply_patterns(df: pd.DataFrame):
    df_analysis = apply_candle_properties(df)
    set_candle_patterns(df_analysis)

    return df_analysis