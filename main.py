import streamlit as st 
from affected_model import infer as inf
from PIL import Image
import pandas as pd
from nlpmodel import infer as nlp
import plotly.graph_objects as go
import warnings

warnings.filterwarnings( "ignore")

affectedpopulation = 10

def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 3])
    # Display field name with some alignment
    c1.markdown("##")
    c1.markdown(label)
    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)
    # Forward text input parameters
    return c2.text_input("", **input_params)

st.sidebar.image('earthquake.jpg',width= 250)
st.sidebar.write('Disaster Response Assistant')
selection = st.sidebar.selectbox("Go to page:", [ 'Home', 'Earthquake Information' , 'Estimate Food and shelter items', 'Chatbot Assistance', 'Further Scope & Credits'])

st.title('Disaster Response Assistant')

#Home page
if selection == 'Home':
    st.title('Home Page')
    st.header('Earthquake Response')
    st.markdown("Welcome to the AI for Disaster Response Assistant! This application was developed by the [AI Wonder Girls team](https://www.linkedin.com/company/80952123/) and focuses on the case study for Earthquake Response.") 
    st.image('images/unsplash1.jpg', caption='Image Credits: unsplash', width= 350)
    st.write("When disaster strikes, both humanitarian organizations and local communities need to coordinate efforts to bring quick help to affected populations.")

    st.write("The  Disaster Response Assistant applies multiple AI techniques to support faster disaster response operations during earthquake emergencies.")

    st.write("The applications aims to help:")
    
    st.markdown('- *Humanitarian agents looking to improve  disaster response logistics operations*') 
    st.markdown('- *Civilians searching for reliable information on first aids and disaster preparedness*') 
    st.markdown('- *Decision makers who can find overall information about earthquakes from established databases*') 
    st.markdown("The application was developed for the [AWS Disaster Response Hackathon](https://awsdisasterresponse.devpost.com/) and is currently hosted as an open source project by the AI Wonder Girls team, which plans to expand it to address other disasters types") 
    st.markdown('More information about the project can be found at: [https://devpost.com/software/ai-wonder-girls-disaster-response](https://devpost.com/software/ai-wonder-girls-disaster-response)')
 
# Earthquake info page       
elif selection == 'Earthquake Information':
    st.title('Earthquake Information')
    st.write('Earthquake are violent and abrupt shaking of the ground, caused by movement between tectonic plates along a fault line in the earth’s crust.')
    st.write('Apart from their extreme potential damage caused by ground shaking, earthquakes can also cause collateral disasters such as landslides, avalanches, fires and tsunamis.')      
    st.write('According to the World Health Organization (WHO), the level of damage caused by earthquakes are commonly associated to their:')
    st.markdown('> *magnitude, intensity and duration,  the local geology, the time of day when it occurs,  building and industrial infrastructure, the risk-management measures put in place.*')
    
    st.header('Impact on Local Communities')
    st.markdown('Earthquakes account for more than halth of the deaths related to natural disasters in the past decades. Between 1998-2017, earthquakes caused nearly 750 000 deaths globally, amd left more than 125 million people affected.')
    st.write('Depending on the magnitude of the events, earthquakes can cause minor to massive damage. In the table below, based on the USGS information, some of the damages are listed:')
    
    #Table
    df = pd.DataFrame(columns=['magnitude', 'shaking', 'damage'])
    df = df.append({'magnitude': '1.0-3.0', 'shaking': 'not felt', 'damage': 'not felt except by specific conditions'}, ignore_index=True)
    df = df.append({'magnitude': '3.0-3.9', 'shaking': 'weak', 'damage': 'can be felt noticebly indoors, especially in upper floors.'}, ignore_index=True)
    df = df.append({'magnitude': '4.0-4.9', 'shaking': 'light/moderate', 'damage': 'felt indoors by many, outdoors by few. Dishes, doors, windows disturbed or broken, walls make cracking sounds.'}, ignore_index=True)
    df = df.append({'magnitude': '5.0-5.9', 'shaking': 'strong/very strong', 'damage': 'felt by all. Slight damage, moving of heavy furniture, moderate damage in ordinary structures, considerable damage in poorly built structures.'}, ignore_index=True)
    df = df.append({'magnitude': '6.0-6.9', 'shaking': 'severe/violent', 'damage': 'considerable damage in ordinary buildings with partial collapse, severe damage in poorly built structures. Fall of chmneys, monuments and walls.'}, ignore_index=True)
    df = df.append({'magnitude': '7.0 and higher', 'shaking': 'extreme', 'damage': 'ranges from destruction of foundations, bridges and rails to total damage in most extreme cases.'}, ignore_index=True)
    st.table(df)

    st.write('During the emergency, earthquakes can leave persons injured, homeless, displaced or evacuated. The financial impact of such events will depend not only on the magnitude of the earthquakes, but also on the development level of the region and local measures prevention of damages. In extreme situations, the financial damage can reach millions of US dollars.')

    st.header('Earthquakes Worldwide')
    st.write('It is estimated that every year, about 20,000 earthquakes take place around the globe (approximately equivalent to 55 per day).')
 
    st.write("Below we can see all earthquakes recorded in the USGS dataset in the last decades.")
    earthquake = pd.read_csv("data/df_merged_all.csv")
    year_start_temp, year_end_temp = st.slider('Choose year range:', 1960, 2020, (1960, 2021))
    
    filter_mag = {'all':[5.0, 15.], '5.0-5.4': [5.0, 5.5], '5.5-5.9': [5.5, 6.0], '6.0-6.4': [6.0, 6.5], '6.5-6.9': [6.5, 7.], '7 or more': [7.0, 15.0]}
    magnitude = st.selectbox("Select a magnitude:", filter_mag.keys())
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x = earthquake.loc[(earthquake['Year'] >= year_start_temp) & (earthquake['Year'] <= year_end_temp) & earthquake['mag'].isin(filter_mag[magnitude])]['country']))
    fig.update_layout(title='Earthquakes worldwide per magnitude range')
    fig.update_xaxes(title_text="Countries")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, use_container_width=True)  
    
    st.write('Around the globe, Asia is the continent most affected by earthquakes, due to its location in a very active seismic area.')
    st.image('data/eda/continent.png', width= 550)
    st.write('The countries most affected by earthquakes are:')
    st.markdown('1. **China:** located between the two largest seismic belts (circum-Pacific and the circum-Indian seismic belts). Squeezed by the Pacific plate, the Indian plate and the Philippine plate, the seismic fracture zones are well developed in this area.')
    st.markdown('2. **Indonesia:** located close to the Ring of Fire region.*')
    st.markdown('3. **Iran:** located where the Eurasian and Arabian tectonic plates meet.*')
    st.markdown('4. **Turkey:** located at the boundary of impact between the Eurasian and Arabian plates.')
    st.markdown('5. **Japan:** located on the joint of four different tectonic plates (North America plate, Pacific plate, Philippine plate, and the Eurasian plate), near the Ring of Fire region.')
    st.markdown('6. **Peru:** at the interface between the South American and Nazca plates.')
    st.markdown('7. **United States:** partially located at the Pacific Ring of Fire, where  tectonics plate are active (boundary of the Pacific and North American plates)')
    st.markdown('8. **Italy:** southern part of the country situated at region where the Eurasian and African plates collide.')
    st.write('Our exploratory data analysis of the USGS dataset shows the earthquakes in the workd since 1960 also in terms of magnitude.')
    st.image('data/eda/world_map.png', width= 500)
 

    st.subheader('Sources')
    st.markdown('[World Heath Organization](https://www.who.int/health-topics/earthquakes#tab=tab_1)') 
    st.markdown('[USGS.gov](https://www.usgs.gov)') 
    st.markdown('[Federal Reserve Bank of Kansas City](https://www.kansascityfed.org/oklahomacity/oklahoma-economist/2016q1-economic-damage-large-earthquakes/)') 
    st.markdown('[Plate Tectonics Wikipedia](https://en.wikipedia.org/wiki/Plate_tectonics)') 
    st.markdown('[FEMA Risk Management](https://www.fema.gov/emergency-managers/risk-management/earthquake)')
    st.markdown('[Kepu.net](http://www.kepu.net.cn/english/quake/outline/index.html)') 


# Relief Package page
elif selection == 'Estimate Food and shelter items':
    st.image('images/package.jpg', caption='Image Credits: Credit:sustainablefood.yale.edu', width=400)
    st.markdown('This application applies a Machine Learning model to determina the number of affected in a given earthquake event, and further uses these estimations to recommend the amounts of food and non-food items for a *Relief Package* based on the [United Nations guidelines for food and nutrition during emergencies](https://www.unhcr.org/45fa745b2.pdf).')
    st.markdown('The app can be used by humanitarian agents for large scale disaster response operations and also by civilians who wish to prepare themselves for the emergency.')
     
    st.subheader('Estimate Food and shelter items') 
    c1, c2, c3,c4 = st.columns(4)
    with c1:
        country = c1.selectbox('Country',('Nepal','Turkey','Chile'))
        #country = c1.selectbox('Country',('China','Indonesia','Iran','Turkey','Japan','Peru','US','Italy','Afghanistan'))
    with c2:
        magnitude = c2.selectbox('Magnitude',(4,4.5,5,5.5,6,6.5))
        # print(magnitude)
    #with c3:
        #mmi = c3.selectbox('MMI',('1','2','3','4','5','6'))
    affectedpopulation = 0
    details = {}
    btnResult = st.button("Estimate Relief Items")
    if btnResult:
        if country == 'Nepal':
            details = {
            'depth' :21,
            'mag':magnitude,
            'mmi':6.2,
            'Population density (people per sq. km of land area)':150,
            'Rural population (% of total population)':87,
            'Urban population (% of total population)':13,
            'GDP growth (annual %)':4
            }         
        elif country == 'Turkey':
            details = {
            'depth' :15.5,
            'mag':magnitude,
            'mmi':7,
            'Population density (people per sq. km of land area)':76,
            'Rural population (% of total population)':40,
            'Urban population (% of total population)':60,
            'GDP growth (annual %)':5.6
            }          
        else:
            details = {
            'depth' :40,
            'mag':magnitude,
            'mmi':6,
            'Population density (people per sq. km of land area)':20,
            'Rural population (% of total population)':16,
            'Urban population (% of total population)':84,
            'GDP growth (annual %)':5
            }           
        df_col = pd.DataFrame(details,index = ['a'])      
        affectedpopulation_df = inf.predictAffected(df_col)
        affectedpopulation = affectedpopulation_df[0]

    with st.expander("Enter the number of affected people manually"):
        with st.form(key='my_form'):
            input = st.text_input(label='Affected Population')
            submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                affectedpopulation = int(input)

       
    if affectedpopulation != 0:
        st.write('Affected population by EarthQuake : ' + str(affectedpopulation))
        st.subheader('NON-FOOD RELIEF ITEMS')
        rounded_population = round(1 * affectedpopulation)
        ClothingandBedding  = rounded_population
        Mattress = rounded_population
        BathingSoap = rounded_population
        LaundrySoap = rounded_population
        Toothbrush = rounded_population
        Toothpaste = rounded_population
        Shampoo = rounded_population
        water = 2.7 * affectedpopulation
        rice = 420 * affectedpopulation
        lentils = 50 * affectedpopulation
        meat = 20 * affectedpopulation
        oil = 25 * affectedpopulation
        sugar = 20 * affectedpopulation
        salt = 5 * affectedpopulation
        biscuits = 125 * affectedpopulation
        milk = 10 * affectedpopulation
        nonfoodData = {
        'Clothing/Bedding' : ClothingandBedding,
        'Mattresses/Mats' : Mattress,
        'Bathing Soap' : BathingSoap,
        'Laundry Soap': LaundrySoap,
        'Toothbrush':Toothbrush,
        'Toothpaste':Toothpaste,
        'Shampoo':Shampoo
        }
        df = pd.DataFrame(list(nonfoodData.items()), index=['1', '2', '3','4','5','6','7'], columns=['Non Food Items', 'Total Quantity based on per person'])
        st.dataframe(df,600, 300)
        st.subheader('FOOD RELIEF ITEMS')
        foodData = {
        'Clean Drinking Water(in litres)' : water,
        'Cereals(Wheat,Rice,Maize in grams)' : rice,
        'Legumes(Beans,Lentils in grams)'  : lentils,
        'Meta/Fish(in grams)': meat,
        'Cooking oil(in grams)':oil,
        'Sugar(in grams)':sugar,
        'Salt(in grams)':salt,
        'High-Energy Biscuits(in grams)':biscuits,
        'Milk Powder(in grams)':milk
        }
        df1 = pd.DataFrame(list(foodData.items()), index=['1', '2', '3','4','5','6','7','8','9'], columns=['Food Items', 'Quantity based on person per day'])
        st.dataframe(df1,600, 300)
       
elif selection=='Chatbot Assistance':
    st.image('images/unsplash2.jpg', caption='Image Credits: Credit: unsplash', width=350)
    st.write('Ask questions related to earthquake response to the chatbot. The assistant is trained with AI models on a curated list of reliable sources about first aids and earthquake emergencies to ensure that important information comes to the ones in need and prevent the spread of false information during emergencies. ')
    st.title('Chatbot Help')
    with st.expander("Earthquake Assistance"):
            input = st.text_input("Type your query here - ", value="", key = 1)
            if  input != "":
                output = nlp.predict(input, "earthquake")
                st.write(output)
    with st.expander("First Aid Assistance"):
            input = st.text_input("Type your query here - ", value="", key = 2)
            if  input != "":
                output = nlp.predict(input, "firstaid")
                st.write(output)

else:
    st.title('Next Steps and Credits')
    st.markdown('This project was developed by the AI Wonder Girls team based. The solution for the relief package is inspired on a [similar approach for cyclone response](https://www.crisis-response.com/Articles/593151/AI_for_disaster.aspx) to which one of the members of the team helped to implement. Next steps for this project include making it an open source project and further expansion to other types of disasters and data sources.')
    st.header('Datasets:')
    st.markdown('**Relief Package:** the data used in this part of the applications is open source and comprises 4 large datasets:')
    st.markdown('- **EMDAT dataset:**')
    st.markdown('- **World Bank Indicators dataset:**')    
    st.markdown('- **USGS dataset:**')
    st.markdown('- **Country dataset:**')        

    st.header('Other Sources:')
    st.markdown('**Relief Package:** based on the [United Nations guidelines for food and nutrition during emergencies](https://www.unhcr.org/45fa745b2.pdf)')
    st.markdown('**Chatbot:** the model inference is implemented using data from [earthquakescanada.ca](https://www.earthquakescanada.ca/info-gen/faq-en.php)')
    st.image('images/AIWonderGirlsLogo_small.png', width=200)
    

