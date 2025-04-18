import pandas as pd
from urllib.parse import urlencode
from bs4 import BeautifulSoup as bsp
import requests
import streamlit as st
st.header("Welcome to Food.com : ")
url='https://www.food.com/'
if st.button("Connect to Server"):
    req=requests.get(url)
    if req.status_code!=200:
        st.warning("Error Code. Check after sometime")       
    else:
        st.success("Connection successfully established")
        cont=bsp(req.content,'html.parser')
        main_nav=cont.find('nav')
        item=main_nav.find('ul').find_all('li',class_=['nav-list-item'])
        item_name=[]
        link_site=[]
        sub_item=dict()
        for i in item:
            types=i.find('span')
            type_name=types.text
            item_name.append(type_name)
            if type_name not in sub_item:
                sub_item[type_name]=list()
            #print(item_name)
            val=i.find('ul').find_all('li')
            for i in val:
                link=i.find('a')
                sub_val=link.text.strip()
                link_site.append(url+str(link.get('href')))
                address=url+str(link.get('href'))
                sub_item[type_name].append((sub_val,address))

        # Convert to flat list of dicts
        flat_data = []
        for category, items in sub_item.items():
            for item, link in items:
                flat_data.append({
                    'category': category,
                    'item': item,
                    'link': link
                })
        df=pd.DataFrame(flat_data)
        df.set_index('category',inplace=True)
        from IPython.display import display, HTML


        # Convert link column to clickable HTML anchor tags
        df['link'] = df['link'].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')
        st.subheader("Here is glipmse of our available items : ")
        st.subheader("Go and check the links : ")
        # Display as HTML table with clickable links
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

        st.info("You can download the csv file for future reference : ")

        # Convert DataFrame to CSV (in memory)
        csv = df.to_csv(index=False).encode('utf-8')
        # Add a download button
        st.download_button(
            label="📥 Download Food CSV",
            data=csv,
            file_name='food.csv',
            mime='text/csv'
        )


