import pandas as pd

for f in ['not_paid_out.csv','paid_out.csv']:
	uuids = pd.read_csv(f)

	uuid = uuids['uuid']

	fixed_uuids = []
	for i in range(len(uuid)):
		new_uuid = uuid[i][:8]+'-'+uuid[i][8:12]+'-'+uuid[i][12:16]+'-'+uuid[i][16:20]+'-'+uuid[i][20:32]
		fixed_uuids.append(new_uuid)

	fixed_uuids = pd.DataFrame(fixed_uuids)
	fixed_uuids.to_csv('fixed_'+f, index = False)