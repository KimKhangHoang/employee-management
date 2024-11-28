"""format_money.py - A module that formats money in a country currency
   Author: Kim Khang Hoang
   Date created: 02/08/2023"""

import locale
def FormatMoney(money):
    # Set the locale to the desired country
    locale.setlocale(locale.LC_ALL, 'en_AU.UTF-8')

    # Format the money with the locale
    format_money = locale.format_string("%d", money, grouping=True)
    return format_money
