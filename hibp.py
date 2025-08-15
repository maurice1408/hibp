# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "polars==1.31.0",
#     "pydantic==2.11.7",
#     "pydantic-settings==2.10.1",
#     "requests==2.32.4",
# ]
# ///

import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import requests
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from pydantic import BaseModel, Field

    import polars as pl
    from pydantic import BaseModel, Field
    from typing import Optional,List

    import urllib.parse 

    import asyncio

    import time
    return (
        BaseModel,
        BaseSettings,
        Field,
        SettingsConfigDict,
        mo,
        pl,
        requests,
        urllib,
    )


@app.cell
def _(BaseSettings, SettingsConfigDict):
    class Settings(BaseSettings):
        hibp_api_key: str
        debug: bool = False
        user_agent: str
        version: str = "v3"
        endpoint: str
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
        )
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
def _(requests, settings, urllib):
    async def v3_search(endpoint: str, version: str, hibp_api_key: str, user_agent: str, srch: str) -> dict:

        print(endpoint)

        headers = {'hibp-api-key': settings.hibp_api_key, 'User-Agent': settings.user_agent}

        url = f"{settings.endpoint}/{settings.version}/breachedaccount/{urllib.parse.quote(srch, encoding='utf-8')}?truncateResponse=False"

        # if regex:
        #    qry = urllib.parse.urlencode(qry)

        res = requests.get(url,
                           headers=headers)

        match res.status_code:
            case 200:
                j = res.json()
            case 404:
                j = {}

        return j
    return (v3_search,)


@app.cell
def _(requests, settings, urllib):
    async def v3_stealers(endpoint: str, version: str, hibp_api_key: str, user_agent: str, srch: str) -> dict:

        # print(endpoint)

        headers = {'hibp-api-key': settings.hibp_api_key, 'User-Agent': settings.user_agent}

        url = f"{settings.endpoint}/{settings.version}/stealerlogsbyemail/{urllib.parse.quote(srch, encoding='utf-8')}"

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
                print("No stealer results")
                j = {}
            case _:
                print(f"Status code: {res.status_code}")
                j = {}

        return j
    return


@app.cell
def _(requests, settings, urllib):
    async def v3_pastes(endpoint: str, version: str, hibp_api_key: str, user_agent: str, srch: str) -> dict:

        # print(endpoint)

        headers = {'hibp-api-key': settings.hibp_api_key, 'User-Agent': settings.user_agent}

        url = f"{settings.endpoint}/{settings.version}/pasteaccount/{urllib.parse.quote(srch, encoding='utf-8')}"

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
    return


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
def _(requests, settings):
    def get_latest_breach() -> dict:

        headers = {'hibp-api-key': settings.hibp_api_key, 'User-Agent': settings.user_agent}

        url = f"{settings.endpoint}/{settings.version}/latestbreach"

        res = requests.get(url)

        return res.json()
    return (get_latest_breach,)


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
def _(mo):
    def show_resp(rsp, srch):

        srch_term = mo.stat(label="Search Term", value=srch)
        srch_ent = mo.stat(label="Pwned's Returned", value=len(rsp))

        return mo.hstack(items=[srch_term, srch_ent])
    return (show_resp,)


@app.cell
def _(get_latest_breach):
    latest = get_latest_breach()
    return (latest,)


@app.cell
def _(latest, mo):
    mo.md(
        f"""
    # Latest Breach

    The latest breach added here is **{latest['Title']}**, the breach date was {latest['BreachDate']}

    Number of records in this breach was {latest['PwnCount']:,}

    ## Description

    {latest['Description']}
    """
    )
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
        for b in range(len(breaches_results)):
            bm = BreachModel.model_validate(breaches_results[b])
            all.append(bm)

    mo.accordion(
        {
            "All Breaches": display_results(all)
        }
    )
    return


@app.cell
def _(mo):
    input_srch = mo.ui.text(label="Account:", full_width=True, placeholder="Enter account (email) text")
    srch_button = mo.ui.run_button(label="Go!", tooltip="Click to run search", full_width=True)
    mo.vstack(
        items=[
            input_srch,
            srch_button
        ],align="stretch"
    )
    return input_srch, srch_button


@app.cell
def _(input_srch, srch_button):
    if srch_button.value: 
        srch = input_srch.value
    return (srch,)


@app.cell
async def _(mo, settings, srch, srch_button, v3_search):
    _output = None

    srch_results = {}

    if srch_button.value:
        print(srch)
        with mo.status.spinner(title="searching breaches...") as _spinner:
            srch_results = await v3_search(settings.endpoint,
                                       settings.version,
                                       settings.hibp_api_key,
                                       settings.user_agent,
                                       srch,)
            _spinner.update("Done")

    _output
    return (srch_results,)


@app.cell
def _(show_resp, srch, srch_button, srch_results):
    _stat = None

    if srch_button.value:
        _stat = show_resp(srch_results, srch)

    _stat
    return


@app.cell
def _(BreachModel, srch_button, srch_results):
    l = []
    if srch_button.value:
        if len(srch_results) > 0:
            for i in range(len(srch_results)):
                m = BreachModel.model_validate(srch_results[i])
                l.append(m)
    return (l,)


@app.cell
def _(display_results, l, srch, srch_button):
    r = None

    if srch_button.value:
        r = display_results(l, select_multi=True, label=f"Search for Account: {srch}")

    r
    return (r,)


@app.cell
def _(l, mo, r):
    v = None
    mo.stop(len(l) == 0)
    v = r.value
    v
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
