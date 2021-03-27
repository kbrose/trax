import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import timedelta
import seaborn as sns

POPULATION = 5_822_434  # https://en.wikipedia.org/wiki/Wisconsin
JNJ = {
    "2021-03-22": 43_057,  # This is when they started publishing manufacturer
    "2021-03-25": 51_190,
}


def analyze():
    # Read the CSV file
    df = pd.read_csv("vax.csv", sep="\t", encoding="utf-16")
    df = df.dropna().drop_duplicates()
    df["vax"] = df["Immunization Count"].str.replace(",", "").astype(int)
    df["date"] = pd.to_datetime(df["Day of Vaccination Date"])
    df = df.sort_values(by="date")
    df.reset_index(inplace=True, drop=True)

    # Pull out columns we'll use a lot
    date = df["date"]
    vax = df["vax"]

    # get % of doses that were from JNJ
    try:
        jnj_rate = JNJ[date.max().date().isoformat()] / vax.sum()
    except KeyError:
        raise RuntimeError(
            "Please update the JNJ dict in this file:"
            f"no data found for {date.max().date().isoformat()}"
        )

    # Compute the daily averages
    daily_avg = vax.iloc[-7:].mean()
    last_week = vax.iloc[-14:-7].mean()
    print(
        f"Data up through {date.max().date()}, recent data is usually"
        " corrected to be higher"
    )
    print(
        f"{daily_avg:.0f} average doses per day over past 7 days"
        f" ({daily_avg - last_week:+.0f} compared to 2 weeks ago)"
    )

    doses_needed = (jnj_rate * POPULATION) + ((1 - jnj_rate) * POPULATION * 2)
    weeks_to_done_naive = (doses_needed - vax.sum()) / daily_avg / 7
    done_date_naive = df["date"].max() + timedelta(
        days=weeks_to_done_naive * 7
    )
    print(
        f"{weeks_to_done_naive:.1f} weeks ({done_date_naive:%Y-%m-%d}) "
        "for EVERY PERSON to get fully immunized"
    )

    # DHS says 20% of wisconsinites are under 16 and not currently eligible
    weeks_to_done_age = (POPULATION * 2 * 0.8 - vax.sum()) / daily_avg / 7
    done_date_age = df["date"].max() + timedelta(days=weeks_to_done_age * 7)
    print(
        f"{weeks_to_done_age:.1f} weeks ({done_date_age:%Y-%m-%d}) "
        "for all eligible people (over 16 years old) to get fully immunized"
    )

    plot(date, vax, weeks_to_done_age, daily_avg)


def plot(date, vax, weeks_to_done_age, daily_avg):
    sns.set_theme()
    f, axs = plt.subplots(2, 1, squeeze=True, sharex=True, figsize=(8, 5))
    plot_base(axs, date, vax)
    axs[0].legend()
    axs[1].legend()
    f.savefig("imgs/curr.png")

    f, axs = plt.subplots(2, 1, squeeze=True, sharex=True, figsize=(12, 5))
    line_avg, line_daily, line_cum = plot_base(axs, date, vax)
    extrap_dates, extrap_vax = extrapolate(
        date, vax, math.ceil(weeks_to_done_age * 7)
    )
    axs[0].plot(
        [date.max()] + extrap_dates,
        [daily_avg] * (len(extrap_dates) + 1),
        "--",
        color=line_avg.get_color(),
    )
    axs[0].plot(
        [date.max()] + extrap_dates,
        [vax.iloc[-1]] + extrap_vax.tolist(),
        "--",
        color=line_daily.get_color(),
        alpha=0.4,
    )

    extrapolated_cumsum = extrap_vax.cumsum() + vax.sum()
    axs[1].plot(
        extrap_dates,
        extrapolated_cumsum / (POPULATION * 2 * 0.8) * 100,
        "--",
        color=line_cum.get_color(),
    )
    axs[1].set_ylim([0, 100])
    axs[0].legend()
    axs[1].legend()
    f.savefig("imgs/extrapolated.png")
    plt.show()


def plot_base(axs, date, vax):
    line_avg = axs[0].plot(
        date, vax.rolling(7).mean(), label="7-day moving average"
    )[0]
    line_daily = axs[0].plot(date, vax, label="daily doses", alpha=0.4)[0]

    line_cum = axs[1].plot(
        date,
        vax.cumsum() / (POPULATION * 2 * 0.8) * 100,
        label="% of needed doses given\n(counting only eligible population)",
    )[0]
    return line_avg, line_daily, line_cum


def extrapolate(date, vax, days_to_extrap):
    extrap_dates = [
        date.max() + timedelta(days=n) for n in range(1, days_to_extrap)
    ]
    extrap_vax = pd.Series(
        [vax.iloc[-7:].tolist()[i % 7] for i in range(len(extrap_dates))]
    )
    return extrap_dates, extrap_vax


if __name__ == "__main__":
    analyze()
