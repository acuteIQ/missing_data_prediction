import matplotlib.pyplot as plt
import json
with open('company_sic_vs_employee_num.json') as json_data:
    input_data=json.load(json_data)
print len(input_data['data_points']['x'])
print len(input_data['data_points']['y'])
plt.plot(input_data['data_points']['x'], input_data['data_points']['y'], 'ro')
plt.title('SIC code vs employee number')
plt.xlabel('industry_sic_code')
plt.ylabel('number_of_employees')
plt.show()
