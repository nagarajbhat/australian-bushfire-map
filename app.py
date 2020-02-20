from flask import Flask
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import folium
from folium import plugins






app = Flask(__name__)


@app.route('/')
def index():
	fire_nrt_m6 = pd.read_csv("./data/fire_archive_M6_101673.csv")
	fire_archive_m6 = pd.read_csv("./data/fire_archive_M6_101673.csv")
	fire_nrt_v1 = pd.read_csv("./data/fire_nrt_V1_101674.csv")
	fire_archive_v1 = pd.read_csv("./data/fire_archive_V1_101674.csv")

	df_merged = pd.concat([fire_archive_v1,fire_nrt_v1],sort=True)
	data = df_merged
	df_filter = data.filter(["latitude","longitude","acq_date","frp"])

	df = df_filter[(df_filter['acq_date']>='2019-12-01')&(df_filter['acq_date']<='2020-01-02')] 



	from folium.plugins import HeatMapWithTime
	# A small function to get heat map with time given the data

	def getmap(ip_data,location,zoom,radius):
    
    	#get day list
		dfmap = ip_data[['acq_date','latitude','longitude','frp']]
		df_day_list = []
		for day in dfmap.acq_date.sort_values().unique():
			df_day_list.append(dfmap.loc[dfmap.acq_date == day, ['acq_date','latitude', 'longitude', 'frp']].groupby(['latitude', 'longitude']).sum().reset_index().values.tolist())
    
		# Create a map using folium
		m = folium.Map(location, zoom_start=zoom,tiles='Stamen Terrain',height=500)
		#creating heatmap with time
		HeatMapWithTime(df_day_list,index =list(dfmap.acq_date.sort_values().unique()), auto_play=False,radius=radius, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}, min_opacity=0.5, max_opacity=0.8, use_local_extrema=True).add_to(m)

		return m

	m = getmap(df,[-28,132],3.5,3)
	#m.save('./html/australia_bushfire.html')
	#m
    
	return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
