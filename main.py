import streamlit as st 
import infer
from PIL import Image

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
    ("","Predict Affected Population", "Estimate Food and shelter items", "Earthquake Information")
)

# selection = st.sidebar.selectbox("Go to page:",["Predict Affected Population", "Estimate Food and shelter items", "Earthquake Information"])
if selection == 'Earthquake Information':
    st.title('Earthquake Information')
    st.write(infer.predict())
elif selection == 'Estimate Food and shelter items':
    st.title('Estimated Food and shelter items')
    image = Image.open('earthquake.jpg')
    st.image(image, caption='Relief Package', width=300)
    people = text_field("People affected: ",) 
    water = text_field("Water Bottles : ",) 
    milk = text_field(("Milk Bottles: "))
    rice  = text_field("Rice Bags: ",) 
    lentils = text_field(("Lentil Bags: "))
  


elif selection == 'Predict Affected Population':
    st.title('Population affected by Disaster')
    Country = text_field("Country: ",) 
    Magnitude = text_field("Magnitude of EarthQuake : ",) 
    Year = text_field(("Year of Eathquake: "))
    st.button("Predict Affected People")

    #c1, c2 = st.columns([2,3])
    #with c1:
    #    c1.header("Relief Package")
       
    #with c2:
    #   c2.header('Relief Items')    
    #   c2.text_input('Rice', '20')
    #   username = text_field("Username")
        
else:
    st.title('Main Page')
