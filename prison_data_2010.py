'''
PIT-UN Internship
Week 1
Roberto Balderas, Elena Irish
Incarceration Rates - Men+Women in Texas and United States
'''

import pandas as pd, seaborn as sns, matplotlib.pyplot as plt

# read in data from the Men+Women sheet
incar = pd.read_excel('data/race_ethnicity_gender_2010.xlsx',
                                    sheet_name = 'Men+Women',
                                    skiprows = range(4))

# choose columns
incar_filtered = incar[['Geography'] + 
                [col_name for col_name in incar.columns if 'Incarceration rate' in col_name]].copy()

# change column names
incar_filtered.columns = (['Geography', 'Population at large'] + 
                [col_name.replace('Incarceration rate: ', '') for col_name in incar_filtered.columns[2:]])

# filter to state of Texas
tx_data = incar_filtered[incar_filtered['Geography'] == 'Texas'].copy()

# filter for entire US
us_data = incar_filtered[incar_filtered['Geography'] == 'United States'].copy()

# pivot the us_data columns
us_data_tidy = pd.melt(us_data, id_vars = ["Geography"],
                                var_name = 'race_ethnicity',
                                value_name = 'incarceration_rate')
                                
# change col values into floats
us_data_tidy['incarceration_rate'] = us_data_tidy['incarceration_rate'].astype(float)


# pivot TX data and fix datatypes
tx_data_tidy = pd.melt(tx_data, id_vars = ['Geography'], 
                        var_name = 'race_ethnicity',
                        value_name = 'incarceration_rate')

# change col values into floats
tx_data_tidy['incarceration_rate'] = tx_data_tidy['incarceration_rate'].astype(float)

# merge into one dataframe for plotting
combined_data_tidy = pd.concat([tx_data_tidy, us_data_tidy])
combined_data_tidy.reset_index(inplace=True)

# create list of incarceration rates in descending order for Texas only
re_order = list(tx_data_tidy.sort_values('incarceration_rate', ascending=False)['race_ethnicity'])


# choose colors for bar plot
palette = {'United States':'crimson',
           'Texas':'cadetblue'}

# plot the data into a barplot
ax = sns.barplot(x = 'incarceration_rate',
                 y = 'race_ethnicity',
                 hue = 'Geography',
                 data = combined_data_tidy,
                 order = re_order, # ordering by Texas rates, which are generally higher
                 palette = palette)

# set axis labels
ax.set(xlabel = "Incarceration Rate per 100k", 
       ylabel = "")

# add plot title and subtitle
plt.title('Incarceration Rates\nTexas vs United States', 
         fontsize='large', fontweight='bold')

# change the layout so that the labels are not cut off
plt.tight_layout()

# change legend size and display plot
plt.legend(fontsize = 'large')
plt.show()

