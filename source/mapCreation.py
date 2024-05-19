import folium
from source.databaseConnection import database

class createHarareMap:
    
    def map():
        # Database Connection
        connection = database(host="localhost", user="root", password="edmore1", database="irental")
        connection.connect()

        # Center coordinates of Harare Metropolitan Province (replace with exact coordinates if needed)
        latitude = -17.825166
        longitude = 31.053056

        # Create a base map
        map = folium.Map(location=[latitude, longitude], zoom_start=10)
        try:
            # Execute the SQL query to fetch coordinates
            points = connection.posts("SELECT ST_Y(coordinates)as latitude, ST_X(coordinates) as longitude FROM irental.coordinates")
            # Fetch all coordinates into a list
            print(points)

            # Add markers for each point
            for point in points:
                folium.Marker([point[0], point[1]]).add_to(map)
            
            map.save("./public/rental/harare.html")

        except Exception as e:
                print("An error occurred:", e)

#createHarareMap.map()