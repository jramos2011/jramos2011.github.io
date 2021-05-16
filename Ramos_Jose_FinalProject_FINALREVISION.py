#!/usr/bin/env python
# coding: utf-8

# ## 2015 Chicago Crimes 
# 
# ### Author: Jose Ramos

# For my final project, I explored the dataset that contained all the **crimes that occured in the city of Chicago during the year of 2015.** The dataset was collected from the `Chicago Data Portal`, in which the dataset can be found by following:
# https://data.cityofchicago.org/Public-Safety/Crimes-2015/vwwp-7yr9
# 
# The dataset presents multiple columns of specific data such as the date of the crime, address, and type of crime. For my visualization, I decided to focus particularly on the district that the crime occured, and what type of crime it was. I believe by doing so, it gives an insight to Chicago residents as to what types of crime occur in the different districts of the city and on how many occasions. This can help in the future as more resources can be provided for districts that are in need, and more awareness is spread about these crimes in the city.

# In[20]:


import bqplot
# for later:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets


# In[21]:


crime_data = pd.read_csv("https://data.cityofchicago.org/resource/vwwp-7yr9.csv")


# In[22]:


crime_data


# In[23]:


dataTable = crime_data.value_counts(["District", "Primary Type"])


# In[24]:


dataTable


# In[25]:


renamed_index = dataTable.reset_index(name = 'counts')
renamed_index


# In[26]:


crime_per_dist = pd.pivot_table(renamed_index,
                            index = ['District'],
                            values = ['counts'],
                            columns = ['Primary Type'],
                            aggfunc = np.sum)


# ### Crime Per District Pivot Table
# The following table, `crime_per_dist` showcases the different crimes that occured for each district in Chicago. The first column list all the districts, in which the following columns shows the different number of crimes that occured per that district alongside the type of crime. This is important in the next step, as I create a interactive heatmap that puts into display the following information.

# In[27]:


crime_per_dist


# In[28]:


crime_types = crime_per_dist.columns.levels[1].to_list()


# In[29]:


crime_types


# In[30]:


col_sc = bqplot.ColorScale(scheme = "RdPu")
x_sc = bqplot.OrdinalScale()
y_sc = bqplot.OrdinalScale()


# In[31]:


final_heat_map = bqplot.GridHeatMap(color = np.log10(crime_per_dist.values),
                             row = crime_per_dist.index, 
                             column = crime_types, 
                             scales = {'color':col_sc,
                                      'row': y_sc,
                                      'column': x_sc},
                             interactions = {'click':'select'},
                             anchor_style = {'fill':'blue'},
                             selected_style = {'opacity': 1.0},
                             unselected_style = {'opacity':1.0})


# In[32]:


c_ax = bqplot.ColorAxis(scale = col_sc, 
                        orientation = 'vertical', 
                        side = 'right')

x_ax = bqplot.Axis(scale = x_sc,
                   label= 'Crime Type', 
                  tick_rotate = 45, #changing the tilt so it could be easier to read
                  tick_style = {'font-size':'3px', #changing the font size of labels in x -axis
                               'tick_offset':'100px',
                               'text_anchor': 'top'})
y_ax = bqplot.Axis(scale = y_sc, 
                   orientation = 'vertical', 
                   label = 'Chicago District',
                  tick_style = {'font-size':'12px'})


# In[33]:


col_sc = bqplot.ColorScale(scheme = "RdPu")
x_sc = bqplot.OrdinalScale()
y_sc = bqplot.OrdinalScale()



c_ax = bqplot.ColorAxis(scale = col_sc, 
                        orientation = 'vertical', 
                        side = 'right')

x_ax = bqplot.Axis(scale = x_sc, label= 'Crime Type', 
                  tick_rotate = 45, #changing the tilt so it could be easier to read
                  tick_style = {'font-size':'3.3px', #changing the font size of labels in x -axis
                               'tick_offset':'100px',
                               'text_anchor': 'top'})
y_ax = bqplot.Axis(scale = y_sc, 
                   orientation = 'vertical', 
                   label = 'Chicago District',
                  tick_style = {'font-size':'12px'})


final_heat_map = bqplot.GridHeatMap(color = np.log10(crime_per_dist.values),
                             row = crime_per_dist.index, #crime_types.index[i or j]
                             column = crime_types, 
                             scales = {'color':col_sc,
                                      'row': y_sc,
                                      'column': x_sc},
                             interactions = {'click':'select'},
                             anchor_style = {'fill':'blue'},
                             selected_style = {'opacity': 1.0},
                             unselected_style = {'opacity':1.0})


mySelectedLabel = ipywidgets.Label()
def get_value(change):
    i,j = change['owner'].selected[0]
    v = np.array(crime_per_dist)[i,j]
    mySelectedLabel.value = 'Number of Crimes in 2015 = ' + str(v)
    i = change['owner'].selected[0]
    z = np.array(crime_types)[j]
    mySelectedLabel.value = 'Number of Crimes in 2015 = ' + str(v)+"     " + " Type of Crime: " + str(z)
    
final_heat_map.observe(get_value, 'selected')


# ### Crime per District Heatmap

# Below is the creation of the heatmap that has the `Chicago Districts` on the `y_axis` and the `Crime Types` on the `x-axis`. The crime types are listed below, in order, as a reference. The heat map provides interaction for the user to select a square, which in return, tells you the number of crimes that occured per that district. It also returns the type of crime that has occured. The number reflects the type of crime that is listed on the x-axis. This gives the user a simple and efficient way to acess the **pivot_table** data, in which you can explore each district and each crime for the year of 2015. 

# In[34]:


print("Theft = " + str(crime_per_dist['counts']['THEFT'].sum()))
print("Battery Theft = " + str(crime_per_dist['counts']['BATTERY'].sum()))
print("Criminal Damage = " + str(crime_per_dist['counts']['CRIMINAL DAMAGE'].sum()))


# To get a better understading of the data, I was able to explore which types of crimes occured the most. From using pandas on my dataset, it can be said that **Theft** was the most occured crime in Chicago in the year of 2015. From the data it was said that **220** theft crimes occured. This was followed by **Battery Theft** crimes which occured **171** times alongside **Criminal Damage** that occured **105** times during the year. This is reflected on the heatmap in which the user can see how these 3 columns are darker compared to the other columns on the heat map. As a remidner, the darker the square, the more significant the number of crimes is.

# `Reference:`
# - **Theft** -> Second to last column
# - **Battery Theft** -> Third column
# - **Narcotics** -> Nineteenth column

# In[35]:


fig = bqplot.Figure(marks = [final_heat_map], axes = [c_ax,y_ax,x_ax])
myDashboard = ipywidgets.VBox([mySelectedLabel,fig])
myDashboard


# In[36]:


crime_types


# ### Important Note:
# In the process of creating my visualization, I imported the CSV directly from the `Chicago Data Portal`. When I imported the data, I was only given 1000 rows in comparasion to the full dataset found on the website. This is a slight error in data in which for the future, I would try to include all the data points within the project. Nevertheless, the sample given in this project gives the story of the larger data set, in which the common crimes remain the same.

# ## Crimes - 2001 to Present in Chicago 

# ### Department, C. P. (2021, May 10). Crimes - 2001 to Present: City of Chicago: Data Portal. Chicago Data Portal. https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2. 

# The following visualization, providing by the **Chicago Police Department**, showcases the number and types of crimes that has occured from 2001 to present day in Chicago. The histogram is able to show the audience that **Theft** was still the most occured crime in the past 20 years, followed by **Battery Theft** and **Criminal Damage**. This is exactly the results we got from our dataset and heatmap for the `year of 2015`, in which the data shares a story about the common crimes associated from the city. In other words, the story from the data points out that **theft** is common throughout the city of Chicago, in which more resources and surveillance might be needed in order to prevent future crimes of this type. Futhermore, this type of data can help law enforcement in the future, as they know what the common crimes have been occuring in the past years. Lastly, the data from both the heatmap and the following visualization gives an insight to the public about their districts and what types of crimes are occuring. 

# ![Screen%20Shot%202021-05-03%20at%204.47.41%20PM.png](attachment:Screen%20Shot%202021-05-03%20at%204.47.41%20PM.png)

# `Link`: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2

# ## Percent of Crimes Cleared by Arrest, 2015

# ### FBI. (2016, June 17). National Data. FBI. https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015/offenses-known-to-law-enforcement/clearances/national-data. 

# The next visualization comes from the FBI, in which it describes the percent of crimes that were cleared by arrest or exceptional means in 2015. The data for the visualization is on a nationwide scale. From this, it can be seen that **murder** and **nonnegligent manslaughter** were the most common crimes that were cleared by arrest in 2015. In other words, this was the most common crime that police had to intervene with force/arrest. Although the visualization does not describe which crimes occured the most in general, it gives the audience an idea that the most **violent crimes were due to murder on a national scale in the year of 2015.** Perhaps this is a visulization that can be done in the future for the city of Chicago, in which it could give the public an idea of what crimes the police had intervene in with arrest or exceptional means. It can provide a different story for Chicago, and give futher insgihts to violent crimes in the city.

# ![Screen%20Shot%202021-05-04%20at%206.13.07%20PM.png](attachment:Screen%20Shot%202021-05-04%20at%206.13.07%20PM.png)

# `Link`: https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015/offenses-known-to-law-enforcement/clearances/national-data

# ### References 

# Department, C. P. (2021, May 10). Crimes - 2001 to Present: City of Chicago: Data Portal. Chicago Data Portal. https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2. 
# 
# FBI. (2016, June 17). National Data. FBI. https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015/offenses-known-to-law-enforcement/clearances/national-data. 
