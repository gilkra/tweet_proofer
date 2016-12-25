import pandas as pd

all_data = pd.read_csv('sample_data.csv')


driver_dict = {}
for i, key in enumerate(all_data['uuid']):
	driver_dict[key] = (all_data['participated'][i],all_data['qualified'][i])

print driver_dict[1]
	
for gb in 


# driver_dict  = [uuid:(qualified,payout)]


	 
	