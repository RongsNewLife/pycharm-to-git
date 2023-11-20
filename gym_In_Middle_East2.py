
import requests
import openpyxl

# actual Google Places API key
API_KEY = 'AIzaSyA5u4UCTjdvpDOI31nxIwmg7qCYoLBKuxY'

# Define the base URL for the Google Places API
BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

# Create a new Excel workbook and worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Define the header row
header = ["Name", "Address", "Website", "Phone"]

# Write the header row to the worksheet
worksheet.append(header)

# Define the latitude and longitude ranges
latitude_range = range(11799174, 31547791, 300000)
longitude_range = range(51850770, 58280315, 300000)

# Iterate through the latitude and longitude ranges
for latitude in latitude_range:
    for longitude in longitude_range:
        # Calculate the latitude and longitude in decimal format
        lat_decimal = latitude / 1000000.0
        lon_decimal = longitude / 1000000.0

        # Define the parameters for the search
        params = {
            'location': f'{lat_decimal},{lon_decimal}',
            'radius': 50000,  # You can adjust the radius as needed
            'keyword': 'gym',
            'key': API_KEY
        }

        # Make a request to the API
        response = requests.get(BASE_URL, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])

            # Iterate through the gyms and add them to the worksheet
            for place in results:
                name = place.get('name', 'N/A')
                address = place.get('vicinity', 'N/A')

                # Use the place_id to fetch details about the gym, including website and phone
                detail_params = {
                    'placeid': place['place_id'],
                    'key': API_KEY
                }

                detail_response = requests.get('https://maps.googleapis.com/maps/api/place/details/json',
                                               params=detail_params)
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    website = detail_data['result'].get('website', 'N/A')
                    phone = detail_data['result'].get('formatted_phone_number', 'N/A')
                    print(f'Name: {name}\nWebsite: {website}\n')
                    worksheet.append([name, address, website, phone])

# Save the workbook to an Excel file
workbook.save("nutritionist_In_US4.xlsx")