# Trax

Naive tracking of Wisconsin's vaccination progress.

I am not an expert, there's probably many reasons why the statistics I report here are incorrect.

Raw data was obtained from https://www.dhs.wisconsin.gov/covid-19/vaccine-data.htm. See below for instructions.

# Current estimates

```
$ python trax.py
Data up through 2021-03-28, recent data is usually corrected to be higher
50030 average doses per day over past 7 days (+2945 compared to 2 weeks ago)
25.2 weeks (2021-09-20) for EVERY PERSON to get fully immunized
18.8 weeks (2021-08-06) for all eligible people (over 16 years old) to get fully immunized
```

# Charts

Current vaccination progress.

![current vaccination progress](./imgs/curr.png)

---

Current vaccination progress extrapolated out to 100% completion (of people who are eligible for the vaccine) using the a rolling 7 day average. Dashed lines are the extrapolations.

![extrapolated vaccination progress](./imgs/extrapolated.png)

# Update data

1. Go to https://www.dhs.wisconsin.gov/covid-19/vaccine-data.htm
2. Under "Vaccine Distribution Summary" section, click "Download", make sure you're on "Allocation and Administration" tab within the tablue view, not the "Providers" tab.
3. Hit "cross tab"
4. Hover over each option until you see the one called "AdministeredByDay", check it
5. Select CSV for the format
6. Click Download
7. Click Download again, or copy the download link into a `curl` command. Either way, save it to the `vax.csv` file

# Why?

Tons of news sites, and even official government sites, only share the current progress. ~~They do not estimate when the vaccinations will be completed if the current vaccination rates continue.~~ I got tired of doing the calculation by hand, so I wrote a simple script to do it for me.

_EDIT:_ This is no longer true. On March 23rd, [NPR started having predictions](https://www.npr.org/sections/health-shots/2021/01/28/960901166/how-is-the-covid-19-vaccination-campaign-going-in-your-state) at a national level of when the vaccinations will be complete. NPR also cites researchers saying that herd immunity can be expected when the population is around 70%-85% vaccinated.
