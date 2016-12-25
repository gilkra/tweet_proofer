
import pandas as pd
import numpy as np

uuids = pd.read_csv('calc_didnt_drive.csv')

all_id = uuids['All']
not_paid = uuids['Not_Paid']
paid = uuids['Paid']

new_list = list(set(all_id)-set(not_paid)-set(paid))

new_list = pd.DataFrame(new_list)
new_list.to_csv('didnt_drive.csv', index = False, header=False)