sales_ranges=[
    {'min': 0, 'max': 499, 'symbol': 'A'},
    {'min': 500, 'max': 999, 'symbol': 'B'},
    {'min': 1000, 'max': 2499, 'symbol': 'C'},
    {'min': 2500, 'max': 4999, 'symbol': 'D'},
    {'min': 5000, 'max': 9999, 'symbol': 'E'},
    {'min': 10000, 'max': 19999, 'symbol': 'F'},
    {'min': 20000, 'max': 49999, 'symbol': 'G'},
    {'min': 50000, 'max': 99999, 'symbol': 'H'},
    {'min': 100000, 'max': 499999, 'symbol': 'I'},
    {'min': 500000, 'max': 999999, 'symbol': 'J'},
    {'min': 1000000, 'max': float('inf'), 'symbol': 'K'}
]

def get_revenue_range(value, range_type='index'):
    for sr_index, sr in enumerate(sales_ranges):
        if sr['min'] <= value and value <= sr['max']:
            if range_type == 'index':
                return sr_index
            else:
                return sr['symbol']

    raise Exception( str('get_revenue_range broke! ' + str(value) + ' sales_ranges ' + str(sales_ranges)) )


employee_ranges=[
    {'min': 0, 'max': 4, 'symbol': 'A'},
    {'min': 5, 'max': 9, 'symbol': 'B'},
    {'min': 10, 'max': 19, 'symbol': 'C'},
    {'min': 20, 'max': 49, 'symbol': 'D'},
    {'min': 50, 'max': 99, 'symbol': 'E'},
    {'min': 100, 'max': 249, 'symbol': 'F'},
    {'min': 250, 'max': 499, 'symbol': 'G'},
    {'min': 500, 'max': 999, 'symbol': 'H'},
    {'min': 1000, 'max': 4999, 'symbol': 'I'},
    {'min': 5000, 'max': 9999, 'symbol': 'J'},
    {'min': 10000, 'max': float('inf'), 'symbol': 'K'},
]

def get_employee_range(value, range_type='index'):
    for sr_index, sr in enumerate(employee_ranges):
        if sr['min'] <= value and value <= sr['max']:
            if range_type == 'index':
                return sr_index
            else:
                return sr['symbol']

    raise Exception( str('get_employee_range broke! ' + str(value) + ' employee_ranges ' + str(employee_ranges)) )
