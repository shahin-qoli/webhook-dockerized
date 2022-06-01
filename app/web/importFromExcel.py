import pandas as pd
from sqlalchemy import create_engine

from web.models import PriceLists, Prices, Brands


def PriceList(request):
    PriceLists.objects.all().delete
    df = pd.read_excel('C:\shahin\z-i\pricelist.xlsx')
    df.columns = [c.lower() for c in df.columns]  # PostgreSQL doesn't like capitals or spaces
    df_reset = df.set_index('id')

    engine = create_engine('postgresql://postgres:@localhost:5432/SpreeWebhook2')

    df_reset.to_sql('web_pricelists', engine,if_exists='append')


def Price(request):
    Prices.objects.all().delete
    df = pd.read_excel('C:\shahin\z-i\price.xlsx')
    df.columns = [c.lower() for c in df.columns]  # PostgreSQL doesn't like capitals or spaces
    df_reset = df.set_index('id')

    engine = create_engine('postgresql://postgres:@localhost:5432/SpreeWebhook2')

    df_reset.to_sql('web_prices', engine,if_exists='append')


def Brand(request):
    Brands.objects.all().delete
    df = pd.read_excel('C:\shahin\z-i\crand.xlsx')
    df.columns = [c.lower() for c in df.columns]  # PostgreSQL doesn't like capitals or spaces
    df_reset = df.set_index('option_value_id')

    engine = create_engine('postgresql://postgres:@localhost:5432/SpreeWebhook2')

    df_reset.to_sql('web_brands', engine,if_exists='append')
