import json
import numpy as np
with open('company_sic_vs_employee_num.json') as json_data:
    input_data=json.load(json_data)
print len(input_data['data_points']['x'])
print len(input_data['data_points']['y'])

nan_count=0
for x_index, x in enumerate(input_data['data_points']['x']):
    if np.isnan(x)  or np.isnan(input_data['data_points']['y'][x_index]):
        nan_count += 1
print nan_count
