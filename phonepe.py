import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json


# DataFrame Creation

# SQL Connection 

connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
mycursor=connection.cursor()
 
# aggre_insurance_df

mycursor.execute("select * from aggregated_insurance")

table1=mycursor.fetchall()
connection.commit()

Aggre_insurance=pd.DataFrame(table1,columns=("State","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

# aggregated_transaction-df

mycursor.execute("select * from aggregated_transaction")

table2=mycursor.fetchall()
connection.commit()

Aggre_transaction=pd.DataFrame(table2,columns=("State","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

# aggregated_user_df

mycursor.execute("select * from aggregated_user")

table3=mycursor.fetchall()
connection.commit()

Aggre_user=pd.DataFrame(table3,columns=("State","Years","Quarter","Brand","Count","Percentage"))

# map_insurance_df

mycursor.execute("select * from map_insurance")

table4=mycursor.fetchall()
connection.commit()

Map_insurance=pd.DataFrame(table4,columns=("State","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

# map_transaction_df

mycursor.execute("select * from map_transaction")

table5=mycursor.fetchall()
connection.commit()

Map_transaction=pd.DataFrame(table5,columns=("State","Years","Quarter","Transaction_count","Transaction_amount","Districts"))

# map_user_df

mycursor.execute("select * from map_user")

table6=mycursor.fetchall()
connection.commit()

Map_user=pd.DataFrame(table6,columns=("State","Years","Quarter","AppOpens","Districts","RegisteredUsers"))

# top_insurance_df

mycursor.execute("select * from top_insurance")

table7=mycursor.fetchall()
connection.commit()

Top_insurance=pd.DataFrame(table7,columns=("State","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

# top_transaction_df

mycursor.execute("select * from top_transaction")

table8=mycursor.fetchall()
connection.commit()

Top_transaction=pd.DataFrame(table8,columns=("State","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

# top_user_df

mycursor.execute("select * from top_user")

table9=mycursor.fetchall()
connection.commit()

Top_user=pd.DataFrame(table9,columns=("State","Years","Quarter","Pincodes","RegisteredUsers"))



def Transaction_amount_count_Y(df, year):

    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_amount=px.bar(tacyg,x="State",y="Transaction_amount",title=f"{year} TRANSACTION_AMOUNT",
                            color_discrete_sequence=["green"],height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg,x="State",y="Transaction_count",title=f"{year} TRANSACTION_COUNT",
                            color_discrete_sequence=["blue"],height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for feature in data1["features"]:
            state_name.append(feature["properties"]["ST_NM"])
        state_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data1,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="temps",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="State",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="tropic",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="State",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):

    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.bar(tacyg,x="State",y="Transaction_amount",title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION_AMOUNT",
                            color_discrete_sequence=["green"],height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count=px.bar(tacyg,x="State",y="Transaction_count",title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION_COUNT",
                            color_discrete_sequence=["blue"],height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        state_name=[]
        for feature in data1["features"]:
            state_name.append(feature["properties"]["ST_NM"])
        state_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data1,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="temps",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="State",title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="tropic",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="State",title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

        return tacy

def Aggre_Tran_Transaction_type(df,state):

    tacy=df[df["State"]==state]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",width=600,
                    title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(fig_pie_1)
    
    with col2:
            
        fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",width=600,
                    title=f"{state.upper()} TRANSACTION COUNT",hole=0.5)
        
        st.plotly_chart(fig_pie_2)

## Aggregate User Analysis 1

def Aggre_user_plot_1(df,year):

    aguy=df[df["Years"]==year]
    aguy.reset_index(drop = True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brand")["Count"].sum())
    aguyg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyg,x="Brand",y="Count",title=f"{year} BRANDS AND TRANSACTION COUNT",width=800,
                    color_discrete_sequence=["green"],hover_name="Brand")
    st.plotly_chart(fig_bar_1)

    return aguy

## Aggregate User Analysis 2
def Aggre_user_plot_2(df, quarter):

    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop = True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brand")["Count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg,x="Brand",y="Count",title=f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",width=800,
                        color_discrete_sequence=["blue"])
    st.plotly_chart(fig_bar_1)

    return aguyq

## Aggregate User Analysis 3

def Aggre_user_plot_3(df, state):
    aqyus=df[df["State"]==state]
    aqyus.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(aqyus,x="Brand",y="Count",title=f"{state.upper()} - BRANDS, TRANSACTION COUNT, PERCENTAGE",hover_data="Percentage",
                    width=1000,markers=True)
    st.plotly_chart(fig_line_1)

    #return aqyus

## MAP INSURANCE DISTRICTS

def Map_insur_Districts(df,state):

    tacy=df[df["State"]==state]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_bar_1=px.bar(tacyg, x="Transaction_amount",y="Districts",orientation="h",height=600,
                        title=f"{state.upper()} - DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=["green"])
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(tacyg, x="Transaction_count",y="Districts",orientation="h",height=600,
                        title=f"{state.upper()} - DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=["blue"])
        st.plotly_chart(fig_bar_2)

# MAP USER PLOT 1
def Map_user_plot_1(df, state):

    muy=df[df["Years"]==state]
    muy.reset_index(drop = True, inplace=True)

    muyg=muy.groupby("State")[["AppOpens","RegisteredUsers"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg,x="State",y=["AppOpens","RegisteredUsers"],
                    title=f"{state} REGISTERED USERS AND APPOPENS",height=800,
                        width=1000,markers=True)
    st.plotly_chart(fig_line_1)

    return muy

# MAP USER PLOT 2
def Map_user_plot_2(df, quarter):

    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop = True, inplace=True)

    muyqg=muyq.groupby("State")[["AppOpens","RegisteredUsers"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg,x="State",y=["AppOpens","RegisteredUsers"],
                    title=f"{df["Years"].min()} YEAR {quarter} QUARTER REGISTERED USERS AND APPOPENS",height=800,
                        width=1000,markers=True,color_discrete_sequence=["pink"])
    st.plotly_chart(fig_line_1)

    return muyq

# MAP USER PLOT 3

def Map_user_plot_3(df, state):
    muyqs=df[df["State"]==state]
    muyqs.reset_index(drop = True, inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(muyqs,x="RegisteredUsers",y="Districts",orientation="h",
                                title=f"{state.upper()} REGISTERED USERS",color_discrete_sequence=["orange"])
        st.plotly_chart(fig_map_user_bar_1)
    
    with col2:
        fig_map_user_bar_2=px.bar(muyqs,x="AppOpens",y="Districts",orientation="h",
                                title=f"{state.upper()} APPOPENS",color_discrete_sequence=["pink"])
        st.plotly_chart(fig_map_user_bar_2)


# TOP INSURANCE PLOT 1

def Top_insurance_plot_1(df, state):
    tiy=df[df["State"]== state]
    tiy.reset_index(drop = True, inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_top_insur_bar_1=px.bar(tiy, x="Quarter",y="Transaction_amount",hover_data="Pincodes",height=650,width=600,
                                    title=f"{state.upper()} TRANSACTION AMOUNT",color_discrete_sequence=["green"])
        st.plotly_chart(fig_top_insur_bar_1)
    
    with col2:
        fig_top_insur_bar_2=px.bar(tiy, x="Quarter",y="Transaction_count",hover_data="Pincodes",height=650,width=600,
                                    title=f"{state.upper()} TRANSACTION COUNT",color_discrete_sequence=["pink"])
        st.plotly_chart(fig_top_insur_bar_2)


# TOP 
def Top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop = True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["State" ,"Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg,x="State",y="RegisteredUsers",color="Quarter",title=f"{year} REGISTERED USERS",width=1000,height=800,
                        color_discrete_sequence=["green"],hover_name="State")
    st.plotly_chart(fig_top_plot_1)

    return tuy

# Top User Plot 2

def Top_user_plot_2(df, state):
    tuys=df[df["State"]==state]
    tuys.reset_index(drop = True, inplace=True)

    fig_top_plot_2=px.bar(tuys,x="Quarter",y="RegisteredUsers",color="RegisteredUsers",title=f"{state.upper()} - REGISTERED USERS, PINCODES, QUARTER",width=1000,height=800,
                            color_discrete_sequence=["pink"],hover_data="Pincodes")
    st.plotly_chart(fig_top_plot_2)


## StreamLit
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select=option_menu("Main Menu",["Home","Data Exploration"])
if select=="Home":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:
        
        st.write("****FEATURES :****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Easy Transactions****")
        st.write("****Multiple Payment Modes****")
        st.write("****Bank Balance check****")
        st.write("****PhonePe Merchants****")
        st.write("****Earn Great Rewards****")
elif select=="Data Exploration":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    with tab1:
        method=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])
        
        if method=="Insurance Analysis":

            col1,col2=st.columns(2)

            with col1:

             years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)


        elif method=="Transaction Analysis":

            col1,col2=st.columns(2)

            with col1:

             years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select The State", Aggre_tran_tac_Y["State"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the state", Aggre_tran_tac_Y_Q["State"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)


        elif method=="User Analysis":
            col1,col2=st.columns(2)

            with col1:

             years=st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select The State", Aggre_user_Y_Q["State"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)


    
    with tab2:
        method2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method2=="Map Insurance":

            col1,col2=st.columns(2)

            with col1:

                years=st.slider("Select the year",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_insur_tac_Y=Transaction_amount_count_Y(Map_insurance,years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select The state", Map_insur_tac_Y["State"].unique())

            Map_insur_Districts(Map_insur_tac_Y,states)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("Select the Quarter",Map_insur_tac_Y["Quarter"].min(),Map_insur_tac_Y["Quarter"].max(),Map_insur_tac_Y["Quarter"].min())
            Map_insur_tac_Y_Q=Transaction_amount_count_Y_Q(Map_insur_tac_Y,quarters)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("select one state", Map_insur_tac_Y_Q["State"].unique())

            Map_insur_Districts(Map_insur_tac_Y_Q,states)




        elif method2=="Map Transaction":

            col1,col2=st.columns(2)

            with col1:

                years=st.slider("Select the year",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            Map_tran_tac_Y=Transaction_amount_count_Y(Map_transaction,years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select The state", Map_tran_tac_Y["State"].unique())

            Map_insur_Districts(Map_tran_tac_Y,states)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("Select The Quarter",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Map_tran_tac_Y,quarters)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select the state", Map_tran_tac_Y_Q["State"].unique())

            Map_insur_Districts(Map_tran_tac_Y_Q,states)


            
        elif method2=="Map User":

            col1,col2=st.columns(2)

            with col1:

             years=st.slider("Select The Year",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            Map_user_Y=Map_user_plot_1(Map_user,years)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("Select The Quarter",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q=Map_user_plot_2(Map_user_Y,quarters)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("select the state", Map_user_Y_Q["State"].unique())

            Map_user_plot_3(Map_user_Y_Q,states)
            


    with tab3:
        method3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method3=="Top Insurance":

            col1,col2=st.columns(2)

            with col1:

                years=st.slider("Select year",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_insur_tac_Y=Transaction_amount_count_Y(Top_insurance,years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select The state_y", Top_insur_tac_Y["State"].unique())

            Top_insurance_plot_1(Top_insur_tac_Y,states)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("Select the Quarter",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q=Transaction_amount_count_Y_Q(Top_insur_tac_Y,quarters)



        elif method3=="Top Transaction":

            col1,col2=st.columns(2)

            with col1:

                years=st.slider("Select year",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_tran_tac_Y=Transaction_amount_count_Y(Top_transaction,years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select state", Top_tran_tac_Y["State"].unique())

            Top_insurance_plot_1(Top_tran_tac_Y,states)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("Select Quarter",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Top_tran_tac_Y,quarters)



        elif method3=="Top User":
            
            col1,col2=st.columns(2)

            with col1:
                years=st.slider("Select the year_t",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_Y=Top_user_plot_1(Top_user,years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select state", Top_user_Y["State"].unique())

            Top_user_plot_2(Top_user_Y,states)



