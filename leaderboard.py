import json
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from plotly import express as px


def load_json(fn: str) -> dict:
    with open(fn) as file:
        content = json.load(file)
    return content


def json_to_dataframe(data_json: dict, year: int) -> pd.DataFrame:
    def tokey(k: int, p: int) -> str:
        return f"{k}_{p}"

    index = []
    data = {f"{k}_{p}": [] for k in range(26) for p in range(1, 3)}
    data.update({f"{k}_{p}_delta": [] for k in range(26) for p in range(1, 3)})
    other_keys = ["local_score", "global_score", "stars", "last_star_ts"]
    for key in other_keys:
        data[key] = []
    ignore_empty_members = st.checkbox(
        "Ignore members without participation", value=True
    )
    for _, member in data_json["members"].items():
        if member["stars"] == 0 and ignore_empty_members:
            continue
        index.append(member["name"])
        for key in other_keys:
            data[key].append(member[key])
        completions = member["completion_day_level"]
        for k in range(1, 26):
            start_time = (datetime(year, 12, k) + timedelta(hours=6)).timestamp()
            for p in range(1, 3):
                if str(k) in completions and str(p) in completions[str(k)]:
                    time = completions[str(k)][str(p)]["get_star_ts"]
                    data[tokey(k, p)].append(time)
                    data[tokey(k, p) + "_delta"].append(time - start_time)
                else:
                    data[tokey(k, p)].append(None)
                    data[tokey(k, p) + "_delta"].append(None)
    for k in range(26):
        if np.all(np.array(data[tokey(k, 1)]) == None):
            del data[tokey(k, 1)]
            del data[tokey(k, 2)]
            del data[tokey(k, 1) + "_delta"]
            del data[tokey(k, 2) + "_delta"]
    return pd.DataFrame(data, index)


def add_dt(df: pd.DataFrame):
    for k in range(26):
        if f"{k}_1" not in df.columns:
            continue
        df[f"{k}_dt"] = df[f"{k}_2"] - df[f"{k}_1"]


def custom_score(df: pd.DataFrame, format_key: str):
    scores = list(range(len(df), 0, -1))
    format_score = format_key + "_score"
    df[format_key.format("total") + "_score"] = 0
    for k in range(26):
        if format_key.format(k) not in df.columns:
            continue

        df[format_score.format(k)] = 0
        sorted_vals = df[format_key.format(k)].sort_values()
        for nu, (name, val) in enumerate(sorted_vals.items()):
            if not pd.isna(val):
                df.at[name, format_score.format(k)] = scores[nu]
        df[format_score.format("total")] += df[format_score.format(k)]


def chart(df: pd.DataFrame, format_key: str):
    data = dict()
    for k in range(26):
        if format_key.format(k) not in df.columns:
            continue

        data[k] = df[format_key.format(k)]
    df = pd.DataFrame(data)
    long = df.T.melt(ignore_index=False)
    long.index.name = "Day"
    long.rename(columns={"value": "Score", "variable": "Name"}, inplace=True)
    fig = px.line(long, x=long.index, y="Score", color="Name")
    st.plotly_chart(fig)


def main(fn: str):
    # load data
    cols = st.columns(2)
    year = cols[1].number_input("Current year", 2015, 2024, 2022)
    data_json = load_json(fn)
    df = json_to_dataframe(data_json, year)

    # add custom score
    add_dt(df)
    custom_score(df, "{}_dt")
    custom_score(df, "{}_1")
    custom_score(df, "{}_2")
    for k in range(26):
        if f"{k}_1_score" not in df.columns:
            continue
        df[f"{k}_local_score"] = df[f"{k}_1_score"] + df[f"{k}_2_score"]
    df["total_local_score"] = df["total_1_score"] + df["total_2_score"]
    df = df.sort_values(
        by=["stars", "total_dt_score", "total_local_score"], ascending=False
    )

    # display table
    print_keys = st.multiselect(
        "Which keys should be shown?",
        df.columns,
        [
            "stars",
            "local_score",
            "global_score",
            "total_dt_score",
        ],
    )
    if len(print_keys) == 0:
        print_keys = df.columns
    st.write(df[print_keys])

    # display over time
    chart_keys = {
        "Local score": "{}_local_score",
        "Score part 1": "{}_1_score",
        "Time to part 1": "{}_1_delta",
        "Score part 2": "{}_2_score",
        "Time to part 2": "{}_2_delta",
        "Time diff score": "{}_dt_score",
        "Time diff": "{}_dt",
    }
    chart_key = st.selectbox("What to plot?", chart_keys.keys())
    chart(df, chart_keys[chart_key])


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
