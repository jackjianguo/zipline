#!/usr/bin/env python
#
# Copyright 2015 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from zipline.api import order, symbol
from zipline.finance import commission, slippage
from zipline.utils.run_algo import _run, BenchmarkSpec, run_algorithm


from trading_calendars import get_calendar
import pandas as pd
import os


stocks = ['AAPL', 'MSFT']


def initialize(context):
    context.has_ordered = False
    context.stocks = stocks

    # Explicitly set the commission/slippage to the "old" value until we can
    # rebuild example data.
    # github.com/quantopian/zipline/blob/master/tests/resources/
    # rebuild_example_data#L105
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def handle_data(context, data):
    if not context.has_ordered:
        for stock in context.stocks:
            order(symbol(stock), 9999)
        context.has_ordered = True


def _test_args():
    """Extra arguments to use when zipline's automated tests run this example.
    """
    import pandas as pd

    return {
        'start': pd.Timestamp('2008', tz='utc'),
        'end': pd.Timestamp('2013', tz='utc'),
    }

if __name__ == "__main__":
    # hello 858
    start=pd.to_datetime('2020-01-01', utc=True)
    end=pd.to_datetime('2020-01-10', utc=True)

    # DEFAULT_BUNDLE = 'jj-csvdir-bundle'
    # 'XSHG': XSHGExchangeCalendar, # shanghai
    # trading_calendar = get_calendar('XSHG')
    
    # Index(['a858', 'algo_volatility', 'algorithm_period_return', 'alpha',
    #   'benchmark_period_return', 'benchmark_volatility', 'beta',
    #   'capital_used', 'ending_cash', 'ending_exposure', 'ending_value',
    #   'excess_return', 'gross_leverage', 'long_exposure', 'long_value',
    #   'longs_count', 'max_drawdown', 'max_leverage', 'net_leverage', 'orders',
    #   'period_close', 'period_label', 'period_open', 'pnl', 'portfolio_value',
    #   'positions', 'returns', 'sharpe', 'short_exposure', 'short_value',
    #   'shorts_count', 'sortino', 'starting_cash', 'starting_exposure',
    #   'starting_value', 'trading_days', 'transactions',
    #   'treasury_period_return'],
    #  dtype='object')
    rslt_df = run_algorithm(
        start=start,
        end=end,
        initialize=initialize,
        capital_base=10000,
        handle_data=handle_data,
        data_frequency='daily',
        analyze=None
        # bundle=DEFAULT_BUNDLE,
        # trading_calendar=trading_calendar
    )

    # print(rslt_df.head)
    rslt_df.to_csv('test.csv')
