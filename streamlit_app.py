import streamlit as st
from snowflake.snowpark.functions import col
import requests  

smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)

cnx = st.connection("snowflake")
session = cnx.session()

# Title
st.title(f":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie."""
)

# Name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Select fruits
fruit_options_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients = st.multiselect(
    "Choose up to 5 ingredients",
    fruit_options_dataframe,
    max_selections=5
)

# Insert data
if ingredients and name_on_order:
    ingredients_str = ""
    for ingredient in ingredients:
        ingredients_str += ingredient + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_str + "','" + name_on_order + """')"""
    
    order_submitted = st.button('Submit Order')
    
    # st.write(my_insert_stmt)
    
    if order_submitted:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# Display dataframe
orders_dataframe = session.table("smoothies.public.orders")
st.dataframe(data=orders_dataframe, use_container_width=True)

# Testing
# st.dataframe(data=fruit_options_dataframe, use_container_width=True)
