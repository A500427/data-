# %%
import requests
import pandas as pd

# %%
###Inladen API - kijk naar country code en maxresults
response = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=100&compact=true&verbose=false&key=93b912b5-9d70-4b1f-960b-fb80a4c9c017")



# %%
###Omzetten naar dictionary
responsejson  = response.json()
responsejson

# %%
response.json()

# %%
###Dataframe bevat kolom die een list zijn. 
#Met json_normalize zet je de eerste kolom om naar losse kolommen
Laadpalen = pd.json_normalize(responsejson)
#Daarna nog handmatig kijken welke kolommen over zijn in dit geval Connections
#Kijken naar eerst laadpaal op de locatie
#Kan je uitpakken middels:
df4 = pd.json_normalize(Laadpalen.Connections)
df5 = pd.json_normalize(df4[0])
df4.head()
df5.head()
###Bestanden samenvoegen
Laadpalen = pd.concat([Laadpalen, df5], axis=1)
Laadpalen.head(20)

# %%
df6 = pd.read_csv('laadpaaldata.csv')
print(df6.head(20))

# %%
import pickle
with open("Charging_data.pkl", "rb") as f:
    data_1 = pickle.load(f)
print(type(data_1))
data_1.head(20)

# %%
import requests
import pandas as pd

# Je eigen API-key
my_api_key = '0df8a63b-3e67-496a-823b-50ed47c80a69'

url = "https://api.openchargemap.io/v3/poi/"
params = {
    "output": "json",
    "countrycode": "NL",
    "maxresults": 100,
    "compact": True,
    "verbose": False,
    "key": '0df8a63b-3e67-496a-823b-50ed47c80a69'  
}

response = requests.get(url, params=params)
data = response.json()

Laadpalen = pd.json_normalize(data)
print(Laadpalen.columns.tolist())
df_conn = pd.json_normalize(Laadpalen["Connections"].apply(lambda x: x[0] if x else {}))
Laadpalen_clean = pd.concat([Laadpalen.drop(columns=["Connections"]), df_conn], axis=1)

belangrijke_kolommen = [
    'IsRecentlyVerified',
    'DateLastVerified', 
    'ID',
    'UUID', 
    'DataProviderID', 
    'OperatorID', 
    'UsageTypeID',
    'UsageCost', 
    'Connections', 
    'NumberOfPoints', 
    'StatusTypeID',
    'DateLastStatusUpdate', 
    'DataQualityLevel',
    'DateCreated', 
    'SubmissionStatusTypeID', 
    'AddressInfo.ID', 
    'AddressInfo.Title', 
    'AddressInfo.AddressLine1', 
    'AddressInfo.Town', 
    'AddressInfo.StateOrProvince', 
    'AddressInfo.Postcode', 
    'AddressInfo.CountryID',
    'AddressInfo.Latitude', 
    'AddressInfo.Longitude', 
    'AddressInfo.ContactTelephone1',
    'AddressInfo.RelatedURL', 
    'AddressInfo.DistanceUnit',
    'AddressInfo.AddressLine2',
    'DataProvidersReference'
]

# Check welke kolommen echt bestaan
bestaan_kolommen = [col for col in belangrijke_kolommen if col in Laadpalen_clean.columns]

# Maak de uiteindelijke tabel
tabel = Laadpalen_clean[bestaan_kolommen]

# Bekijk de eerste 10 rijen
print(tabel.head(10))



# %%
print(df4.isna().sum())


# %%
print(df5.isna().sum())


# %%
print(df6.isna().sum())

# ---- GRAFIEK 1: Laadsessies per uur ----
st.subheader("⏰ Laadsessies per uur van de dag")
hourly_counts = df_filtered.groupby("hour").size().reset_index(name="Aantal laadsessies")
fig1 = px.bar(hourly_counts, x="hour", y="Aantal laadsessies",
              title="Aantal laadsessies per uur van de dag")
# Forceer hele getallen op x-as
fig1.update_xaxes(dtick=1)
st.plotly_chart(fig1, use_container_width=True)

# ---- GRAFIEK 2: Totaal geladen energie per maand ----
st.subheader("📅 Totaal geladen energie per maand")
energy_by_month = df_filtered.groupby("month")[energy_col].sum().reset_index().sort_values("month")
fig2 = px.bar(energy_by_month, x="month", y=energy_col,
              title="Totaal geladen energie per maand")
# Maanden zijn categorisch, toon alle ticks
fig2.update_xaxes(type='category')
st.plotly_chart(fig2, use_container_width=True)

# ---- GRAFIEK 3: Totaal geladen energie per jaar ----
st.subheader("📈 Totaal geladen energie per jaar")
energy_by_year = df_filtered.groupby("year")[energy_col].sum().reset_index().sort_values("year")
fig3 = px.bar(energy_by_year, x="year", y=energy_col,
              title="Totaal geladen energie per jaar")
# Hele jaren op x-as
fig3.update_xaxes(dtick=1)  # als x numeriek is
st.plotly_chart(fig3, use_container_width=True)

# ---- EXTRA GRAFIEK (CSV) ----
if file_type == "CSV (.csv)":
    st.subheader("⚡ Gemiddelde laadsnelheid per sessie (kWh/uur)")
    fig4 = px.histogram(df_filtered, x="charge_rate", nbins=20,
                        title="Verdeling van gemiddelde laadsnelheid per sessie")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("🚦 Top 3 laaduren van de dag")
    top_hours = df_filtered.groupby("hour").size().sort_values(ascending=False).head(3).reset_index(name="Aantal sessies")
    fig5 = px.bar(top_hours, x="hour", y="Aantal sessies",
                  title="Top 3 meest gebruikte laaduren")
    # Hele getallen voor uur-as
    fig5.update_xaxes(dtick=1)
    st.plotly_chart(fig5, use_container_width=True)





















