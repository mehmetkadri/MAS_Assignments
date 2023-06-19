import pandas as pd

# read csv named Lib_Data.csv
df = pd.read_csv('Lib_Data.csv')

# create a list that contains a multiplication weight for each month of a year 
monthly_weight = [1.5, 0.6, 1.3, 0.9, 1.6, 1.1, 0.3, 0.3, 0.7, 1.0, 1.4, 0.9]

# set the date column to date type
df['Date'] = pd.to_datetime(df['Date'])

# find the Borrowed_Book_Count column values where date column's value is between 8/1/2022 and 7/31/2023
df_temp = df.copy()
df_temp['Borrowed_Book_Count'] = df[(df['Date'] >= '8/1/2022') & (df['Date'] <= '7/31/2023')]['Borrowed_Book_Count']
df_temp['Returned_Book_Count'] = df[(df['Date'] >= '8/1/2022') & (df['Date'] <= '7/31/2023')]['Returned_Book_Count']
df_temp['Daily_User_Count'] = df[(df['Date'] >= '8/1/2022') & (df['Date'] <= '7/31/2023')]['Daily_User_Count']

Borrowed, Returned, Daily = [], [], []

def multColttw(col_name):
    for i in range(1,13):
        a = df_temp[(df_temp['Date'] >= '10/1/2022') & (df_temp['Date'] <= '10/31/2022')][col_name] * monthly_weight[i-1]
        a = a.astype(int)
        if(col_name == 'Borrowed_Book_Count'):
            Borrowed.append(a)
        elif(col_name == 'Returned_Book_Count'):
            Returned.append(a)
        else:
            Daily.append(a)

for i in ['Borrowed_Book_Count','Returned_Book_Count','Daily_User_Count']:
    multColttw(i)

# create a new dataframe
df_new = pd.DataFrame()

# add date column
for i in range(1,13):
    for j in range(1,32):
        df_new = df_new.append({'Date': str(i) + '/' + str(j) + '/2022'}, ignore_index=True)
        print(str(i) + '/' + str(j) + '/2022')

# add the new columns to the dataframe bt flattening the lists
df_new['Borrowed_Book_Count'] = [item for sublist in Borrowed for item in sublist]
df_new['Returned_Book_Count'] = [item for sublist in Returned for item in sublist]
df_new['Daily_User_Count'] = [item for sublist in Daily for item in sublist]

# save the dataframe to a csv file
df_new.to_csv('Lib_Data_2022.csv', index=False)