# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "polars==1.33.1",
#     "pydantic==2.11.9",
#     "python-dotenv==1.1.1",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.16.4"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import requests


    from pydantic import BaseModel, Field

    from dotenv import dotenv_values
    from dataclasses import dataclass

    import polars as pl
    from pydantic import BaseModel, Field
    from typing import Optional,List

    import urllib.parse 

    import asyncio

    import time
    return BaseModel, Field, dataclass, dotenv_values, pl, requests


@app.cell
def _(dataclass, dotenv_values):
    env_settings = dotenv_values(".env")

    @dataclass
    class Settings():
        hibp_api_key: str = env_settings['hibp_api_key']
        debug: bool =  env_settings['debug']
        user_agent: str =  env_settings['user_agent']
        version: str =  env_settings['version']
        endpoint: str =  env_settings['endpoint']


    settings = Settings()

    if (settings.debug):
        print(settings.hibp_api_key)
        print(settings.debug)
        print(settings.user_agent)
        print(settings.version)
        print(settings.endpoint)
    return (settings,)


@app.cell
def _(BaseModel, Field):
    class BreachModel(BaseModel):
        LogoPath: str
        Name: str
        Title: str
        Domain: str
        BreachDate: str # date	
        AddedDate:	str # datetime	
        ModifiedDate: str #	datetime	
        PwnCount: int
        Description: str
        DataClasses: list = Field(default_factory=list)
        IsVerified: bool
        IsFabricated: bool
        IsSensitive: bool
        IsRetired: bool
        IsSpamList: bool
        IsMalware: bool
        IsSubscriptionFree: bool
        IsStealerLog: bool
    return (BreachModel,)


@app.cell
def _(requests, settings):
    async def v3_breaches(endpoint: str, version: str, hibp_api_key: str, user_agent: str) -> dict:

        # print(endpoint)

        headers = {'hibp-api-key': settings.hibp_api_key, 'User-Agent': settings.user_agent}

        url = f"{settings.endpoint}/{settings.version}/breaches"

        # if regex:
        #    qry = urllib.parse.urlencode(qry)

        res = requests.get(url,
                           headers=headers)

        if (settings.debug):
            print(res.status_code)

        match res.status_code:
            case 200:
                j = res.json()
            case 404:
                print("No pastes results")
                j = {}
            case _:
                print(f"Status code: {res.status_code}")
                j = {}

        return j
    return (v3_breaches,)


@app.cell
def _(conv_to_str, mo, pl):
    def display_results(results, label="", select_multi=False):

        df = pl.DataFrame(results)
        df_str = conv_to_str(df)
        if (select_multi):
            y = mo.ui.table(df_str, selection="multi", label=label)
        else:
            y = mo.ui.table(df_str, selection="single-cell", label=label)
        # s = y.value

        return y
    return (display_results,)


@app.cell
def _(pl):
    def conv_to_str(df):

        join_str = " / "

        return df.with_columns(
            pl.col("BreachDate").cast(pl.Date),
            pl.col("AddedDate").cast(pl.Datetime),
            pl.col("ModifiedDate").cast(pl.Datetime),
            pl.col("DataClasses").cast(pl.List(pl.String)).list.join(join_str)
            )
    return (conv_to_str,)


@app.cell
def _(requests, settings):
    def get_latest_breach() -> dict:

        headers = {'hibp-api-key': settings.hibp_api_key, 'User-Agent': settings.user_agent}

        url = f"{settings.endpoint}/{settings.version}/latestbreach"

        res = requests.get(url)

        return res.json()
    return (get_latest_breach,)


@app.cell
def _(get_latest_breach):
    latest = get_latest_breach()
    return (latest,)


@app.cell
def _(mo):
    hibp_logo = mo.image(
        src="./pwned_logo.png",
        alt="HIBP logo",
        width=220,
        height=70,
        rounded=True
    )



    hibp_link = mo.md(f"""To go to HIBP Search click here ▶︎ [HIBP](https://molab.marimo.io/notebooks/nb_mFFvh3EWS1F97rXMGfmC82/app)""")

    return hibp_link, hibp_logo


@app.cell
def _(latest, mo):
    lb = mo.md(
        f"""
    # Latest Breach

    The latest breach added here is **{latest['Title']}**, the breach date was {latest['BreachDate']}

    Number of records in this breach was {latest['PwnCount']:,}

    ## Description

    {latest['Description']}
    """
    )
    return (lb,)


@app.cell
def _():
    return


@app.cell
async def _(BreachModel, display_results, mo, settings, v3_breaches):
    with mo.status.spinner(title="Fecthing breaches...") as _spinner:
            breaches_results = await v3_breaches(settings.endpoint,
                                       settings.version,
                                       settings.hibp_api_key,
                                       settings.user_agent)
            _spinner.update("Done")

    all = []

    if len(breaches_results) > 0:
        pwned_records = 0
        pwned_websites = len(breaches_results)
        for b in range(len(breaches_results)):
            pwned_records = pwned_records + breaches_results[b]["PwnCount"]
            bm = BreachModel.model_validate(breaches_results[b])
            all.append(bm)

    print(f"pwned_records: {pwned_records}")
    print(f"pwned_websites: {pwned_websites}")

    pwned_summary = mo.hstack([
        mo.stat(value=pwned_websites, label="pwned websites"),
        mo.stat(value=pwned_records, label="pwned records")
        ]
    )
    all_breaches = mo.accordion(
        {
            "All Breaches (click on me to expand / contract)": display_results(all)
        }
    )
    return all_breaches, pwned_summary


@app.cell
def _(all_breaches, hibp_link, hibp_logo, lb, mo, pwned_summary):
    hibp_stack = mo.vstack(
        [
            mo.center(hibp_logo),
            lb, 
            pwned_summary, 
            all_breaches,
            hibp_link
        ])
    return (hibp_stack,)


@app.cell
def _(hibp_stack):
    hibp_stack
    return


@app.cell
def _(mo):
    mo.Html('<hr style="height:5px;border-width:0;color:green;background-color:green">')
    return


@app.cell
def _(mo):
    deh_logo = mo.image(
        src="./deh_logo.png",
        alt="DeHashed",
        rounded=True
    )

    deh_link = mo.md(f"""To go to DeHashed Search click here ▶︎ [DeHashed](https://molab.marimo.io/notebooks/nb_WZCbiNTCQDHXbESFDsFEHv/app)""")


    deh_stack = mo.vstack([
        mo.center(deh_logo),
        deh_link
    ])
    return (deh_stack,)


@app.cell
def _(deh_stack):
    deh_stack
    return


@app.cell
def _(mo):
    mo.Html('<hr style="height:5px;border-width:0;color:green;background-color:green">')
    return


@app.cell
def _(mo):
    gh_logo = mo.image(
        src="./GitHub_Lockup_Dark_60.png",
        alt="GitHub",
        rounded=True
    )

    gh_link = mo.md(f"""To go to GitHub Enumerator click here ▶︎ [GitHub](https://molab.marimo.io/notebooks/nb_CftbEkCLAL9YqzKGkBQHen/app)""")

    gh_stack = mo.vstack([
        mo.center(gh_logo),
        gh_link
    ])
    return (gh_stack,)


@app.cell
def _(gh_stack):
    gh_stack
    return


if __name__ == "__main__":
    app.run()
