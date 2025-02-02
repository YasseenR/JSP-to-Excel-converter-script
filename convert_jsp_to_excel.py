import requests
from bs4 import BeautifulSoup
import pandas as pd

# This python script simply converts a specific JSP Table made by another department.
# This *can* work with any JSP table however, I tailored this script to work with the URL shown below
# Modify script as needed for your URL



# URL of the JSP webpage (This should be changed to whatever URL is needed to be swapped.)
url = 'https://tuportal6.temple.edu/html/TEMPLE/apps/bpi/public/newAccessGrid/newAccessGrid.jsp'  

# Fetch the webpage content
response = requests.get(url)
content = response.content

# Parse the HTML content
soup = BeautifulSoup(content, 'html.parser')

# Find the table (assuming the data is in a table)
table = soup.find('table')

# Check if the table was found
if table is None:
    print("No table found on the webpage.")
    exit()

# Extract table rows (skipping the first row assuming it's the header)
rows = []
data_rows = table.find_all('tr')[1:]  # Skip the first row (header row)
for tr in data_rows:
    cells = []
    for td in tr.find_all(['td', 'th']):
        # Check if the cell contains an element with class "fa fa-times" (Pretty much checking to see if there is an X)
        if td.find(class_="fa fa-times"):
            cells.append("\u2717")
        # Check if the cell contains an element with class "fa fa-check" (Pretty much checking to see if there is a checkmark)
        elif td.find(class_="fa fa-check"):
            cells.append("\u2713")
        # If no X or Checkmark, just copy the text inside and insert into array.
        else:
            cells.append(td.text.strip())
    rows.append(cells)

# Add an empty cell at the beginning of the first row to create an empty top-left cell
if rows:
    rows[0].insert(0, "")

# Create a DataFrame
df = pd.DataFrame(rows)

# Save DataFrame to Excel file
df.to_excel('output.xlsx', index=False, header=False)  # Skip writing headers to Excel file
print("Excel file saved as 'output.xlsx'")

