# -*- coding: utf-8 -*-
"""
@author: Aniket
"""
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

server = 'your_server_name'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'

connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)

connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)

cursor = connection.cursor()

query = "Select 'Qtr ' + Convert(Nvarchar(10),DATEPART(QUARTER,MsgDate)) + ' - ' + Convert(Nvarchar(10),Year(EEOIDet.MsgDate)) as TPeriod, Sum(IsNull(TotalHFO,0)) as TotalHFO ,Sum(IsNull(TotalMDO,0)) as TotalMDO, Sum(IsNull(TotalLSFO,0)) as TotalLSFO, Sum(IsNull(TotalECAGO,0)) as TotalECAGO  ,Sum(CO2Emit) as TotalCO2, Sum(TransportWork) as TotalTransWork, Case When Sum(TransportWork) <> 0 Then  Round((Sum(CO2Emit)*1000000)/Sum(TransportWork),2) Else 0 End as EEOIPeriod  from  dbo.EEOIDet LEFT OUTER JOIN  dbo.VoyNo ON dbo.EEOIDet.ShipID = dbo.VoyNo.ShipID AND dbo.EEOIDet.VoyNo = dbo.VoyNo.VoyNo WHERE (VoyNo.VslLastMsgType IS NOT NULL) and (TotalHFO+TotalMDO+TotalLSFO+TotalECAGO) >0  Group by Year(EEOIDet.MsgDate),DATEPART(QUARTER,MsgDate)  Order by Year(EEOIDet.MsgDate),DATEPART(QUARTER,MsgDate)"
cursor.execute(query)

# Fetch the data into a list of tuples
rows = cursor.fetchall()

# Get column names from the cursor's description
column_names = [column[0] for column in cursor.description]

# Create a DataFrame from the fetched data and column names
dfQtrEEOI = pd.DataFrame.from_records(rows, columns=column_names)
dfQtrEEOI

dfQtrEEOI.info()

# Convert a specific column to float
dfQtrEEOI['EEOIPeriod'] = pd.to_numeric(dfQtrEEOI['EEOIPeriod'], errors='coerce').astype(float)

#Plot the bar graph
ax = dfQtrEEOI.plot(x='TPeriod', y='EEOIPeriod', kind='bar', figsize=(14, 8))
plt.title('Bar Chart: EEOI by Quarter Periods')
plt.xlabel('Quarter Periods')
plt.ylabel('EEOI (gm CO2/t-nm)')
plt.xticks(rotation=45)
plt.tight_layout()

# Add data point labels
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.2f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10),
                textcoords='offset points')

plt.savefig('EEOI_bar_chart.jpg')
    
# Show the plot
plt.show()


