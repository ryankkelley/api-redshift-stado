from pydantic import BaseModel


class TradeDesk(BaseModel):
    vendor: str
    date = str
    creativename: str
    campaignname: str
    flight_start_date: str
    flight_end_date: str

def get_sql(account_id):
    sql = f"""
        SELECT
        'Goodway Group'
        AS
        vendor
        , date
        , creativename
        , campaignname
        , flight_start_date
        , flight_end_date
        , SUM(capped_budget_delivered)
        AS
        capped_budget_delivered
        , SUM(impressioncount)
        AS
        impressions
        , SUM(frequency)
        AS
        frequency
        , SUM(clickcount)
        AS
        clicks
        FROM
        ttd_origin.performancereport_unicorn_plus
        WHERE
        opportunity_id = '{account_id}'
        GROUP
        BY
        vendor
        , date
        , creativename
        , campaignname
        , flight_start_date
        , flight_end_date
        ORDER
        BY
        date,
        campaignname,
        creativename,
        flight_start_date,
        flight_end_date;
        """

    return sql

def get_schema(row):

    schema = {
        'vendor': row[0]['stringValue'],
        'date': row[1]['stringValue'],
        'campaign': row[2]['stringValue'],
        'campaign_line_item': row[3]['stringValue'],
        'flight_start_date': row[4]['stringValue'],
        'flight_end_date': row[5]['stringValue'],
        'budget_delivered': row[6]['doubleValue'],
        'impressions': row[7]['longValue'],
        'frequency': row[8]['longValue'],
        'clicks': row[9]['longValue'],
    }
    return schema