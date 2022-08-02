import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 50)
pd.set_option('display.max_rows', 500)

#reading the csv file
survey_file_input = "survey.csv" 
raw_df = pd.read_csv(survey_file_input)

relevant_data =raw_df[["Age", "Gender", "Country", "state","self_employed", 
                    "remote_work", "tech_company", "family_history", "treatment", 
                    "mental_health_consequence","phys_health_consequence"]]
#Changing the "maybe" value to "yes" in the columns 'mental_health_consequence' and 'phys_health_consequence'

relevant_data.loc[(relevant_data['mental_health_consequence'].isin(['Yes','Maybe'])), "mental_health_consequence"] = "Yes" 
relevant_data.loc[(relevant_data['phys_health_consequence'].isin(['Yes','Maybe'])), "phys_health_consequence"] = "Yes"
print(relevant_data['Gender'].unique())

#cleaning the gender column

l_genders_female = ["Female","female","Cis Female","F","Woman","f","queer/she/they","Femake","woman","Female","cis-female/femme","Female (cis)","femail"]
l_genders_male = ['M', 'Male', 'male','m','Male-ish' ,'maile','something kinda male?','Cis Male','Mal','Male (CIS)','Make','Guy (-ish) ^_^','male leaning androgynous', 'Male ',
'Man','msle','Mail','cis male','Malr','Cis Man','ostensibly male, unsure what that really means']
l_genders_nonbinary = ['Trans-female','non-binary','Nah','All', 'Enby','fluid','p','A little about you','Genderqueer','Androgyne','Agender','queer','Trans woman','Neuter',]

relevant_data.loc[(relevant_data['Gender'].isin(l_genders_female)), "Gender"] = "Female"
relevant_data.loc[(relevant_data['Gender'].isin(l_genders_male)), "Gender"] = "male"
relevant_data.loc[(relevant_data['Gender'].isin(l_genders_nonbinary)), "Gender"] = "Nonbinary"
print(relevant_data)
print(relevant_data["Gender"].head(50))

print(relevant_data['mental_health_consequence'].unique()) 
print(relevant_data['phys_health_consequence'].unique())

#Grouping the AGE category

age_grp = [(relevant_data["Age"] <= 11), (relevant_data["Age"] >= 18) & (relevant_data["Age"] <= 24),
            (relevant_data["Age"] <= 34), (relevant_data["Age"] <= 44), (relevant_data["Age"] <= 50), (relevant_data["Age"] <= 60),(relevant_data["Age"] <= 80)]
values = ['Under 18', 'Under 25', 'Under 35','Under 45','Under 50','Under 60','Under 80']
relevant_data['age_categories'] = np.select(age_grp, values)

relevant_data["Age"] = relevant_data["age_categories"]
print(relevant_data["age_categories"].head(50))

#Grouping the columns
final_data = relevant_data.groupby(["Age", "Gender", "Country", "state","self_employed",
                                        "remote_work", "tech_company","mental_health_consequence",
                                        "phys_health_consequence"]).count().reset_index()
#assert len(relevant_data['Gender'])==3 ,"data cleaned"

#converting the cleaned file to new csv file

import csv
with open('cleaned.csv','w',newline='') as f:
    fieldnames=final_data
    a=csv.DictWriter(f,fieldnames=fieldnames)
    fieldnames.to_csv('transactions.csv', header=False, quoting=csv.QUOTE_NONE, escapechar=' ')

#data visualization using the dash

from dash import Dash, html, dcc
import plotly.express as px
app = Dash(__name__)

fig = px.bar(final_data, x="remote_work", y="self_employed", color="mental_health_consequence", barmode="group")
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)