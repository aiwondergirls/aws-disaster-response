import streamlit as st 
from affected_model import infer as inf
from PIL import Image
import pandas as pd
from nlpmodel import infer as nlp


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

st.title('Disaster Response Assistant')
st.sidebar.image('earthquake.jpg')
selection = st.sidebar.selectbox(
    "what are you searching for?",
    ("","Estimate Food and shelter items", "Earthquake Information")
)

if selection == 'Earthquake Information':
    st.title('Earthquake Information')

    details = {
    'depth' :21,
    'mag':6.0,
    'mmi':6.2,
    'Population density (people per sq. km of land area)':150,
    'Rural population (% of total population)':87,
    'Urban population (% of total population)':13,
    'GDP growth (annual %)':4
    }

    df_col = pd.DataFrame(details,index = ['a'])
   # data = pd.get_dummies(df_col, columns=["country"])
    st.write(inf.predictAffected(df_col))

elif selection == 'Estimate Food and shelter items':
    st.subheader('Estimate Food and shelter items') 
    c1, c2, c3,c4 = st.columns(4)
    with c1:
        country = c1.selectbox('Country',('Nepal','Turkey','Chile'))
        #country = c1.selectbox('Country',('China','Indonesia','Iran','Turkey','Japan','Peru','US','Italy','Afghanistan'))
    with c2:
        magnitude = c2.selectbox('Magnitude',(4,4.5,5,5.5,6,6.5))
    #with c3:
        #mmi = c3.selectbox('MMI',('1','2','3','4','5','6'))
   
    btnResult = st.button("Estimate Relief Items")
    #st.write(magnitude)
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
       
        st.write('Affected population by EarthQuake : ' + str(affectedpopulation))

        st.subheader('NON-FOOD RELIEF ITEMS')
        ClothingandBedding  = 1 * affectedpopulation
        Mattress = 1 * affectedpopulation
        BathingSoap = 1 * affectedpopulation
        LaundrySoap = 1 * affectedpopulation
        Toothbrush = 1 * affectedpopulation
        Toothpaste = 1 * affectedpopulation
        Shampoo = 1 * affectedpopulation

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
    
    #ClothingandBedding  = text_field("Clothing/Bedding: ",) 
    #Mattress = text_field("Mattresses/Mats : ",) 
    #BathingSoap = text_field("Bathing Soap : ",) 
    #LaundrySoap = text_field("Laundry Soap : ",) 
    #Toothbrush = text_field("Toothbrush : ",) 
    #Toothpaste = text_field("Toothpaste : ",) 
    #Shampoo = text_field("Shampoo : ",) 
    #people = text_field("People affected: ",) 
    #water = text_field("Water Bottles : ",) 
    #milk = text_field("Milk Bottles: ",)
    #rice  = text_field("Rice Bags: ",) 
    #lentils = text_field("Lentil Bags: ",)
       
else:
    st.title('Main Page')
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



