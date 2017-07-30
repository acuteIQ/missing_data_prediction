def get_target_col_name(target_type):
    if target_type == 'yearly_sales':
        target_col = 'cast(yearly_sales as numeric)'
    elif target_type == 'number_of_employees':
        target_col = 'number_of_employees'
    elif target_type == 'credit_score':
        target_col = 'efx_creditperc'
    elif target_type == 'business_risk':
        target_col = 'efx_failrate'
    else:
        raise Exception(str('Unknown target_type ' + target_type))

    return target_col


def get_target_col_name_company_prediction(target_type):
    if target_type == 'yearly_sales':
        target_col = 'cast(yearly_sales as numeric)'
    elif target_type == 'number_of_employees':
        target_col = 'number_of_employees'
    elif target_type == 'credit_score':
        target_col = 'credit_score'
    elif target_type == 'business_risk':
        target_col = 'business_risk'
    else:
        raise Exception(str('Unknown target_type ' + target_type))

    return target_col
