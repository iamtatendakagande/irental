import folium
import pandas as pd

companies = pd.read_csv("./static/uploads/coordinates.csv")
companies.head()

# Center coordinates of Harare Metropolitan Province (replace with exact coordinates if needed),
latitude = -17.825166
longitude = 31.053056
# Create a base map,
map = folium.Map(location=[latitude, longitude], zoom_start=11)

for i in range(0, len(companies)):
    folium.Marker([companies.iloc[i]["latitude"],companies.iloc[i]["longitude"]], 
    popup = companies.iloc[i]["address"],  # Assuming a "name" column for popup content
    icon=folium.Icon(color="blue", icon="info-sign")).add_to(map)  # Customize icon"

file_name = 'public/rental/'
map.save(file_name+"harare.html")  # Save the map as an HTML file