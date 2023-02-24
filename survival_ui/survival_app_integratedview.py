import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test
# import pyautogui
# import mpld3
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np


st.set_page_config(layout="wide")



# img=cv2.imread("scientist.png",1)

import base64
from io import StringIO 


st.sidebar.markdown("<h2 align='center' style='color:#ff0000;'>OncoVision</h2>",unsafe_allow_html=True)
st.markdown("<img src='https://www.persistent.com/wp-content/uploads/2021/04/Logo-variants-Logo-tagline.jpg' width='250' height='100' alt='me' align='right'>",unsafe_allow_html=True)
# st.title("minimal residual disease monitoring")
placeholder = st.empty()

# Replace the placeholder with some text:
placeholder.title("Minimal Residual Disease(MRD)  Monitoring")

# Replace the text with a chart:
# placeholder.line_chart({"data": [1, 5, 2, 6]})

# Replace the chart with several elements:
# with placeholder.container():
#     st.write("This is one element")
#     st.write("This is another")



# col1,col2=st.columns(2)

option = st.sidebar.radio(
    'Please select an end user profile: ',
    ('OncoClinician','Doctor', 'Bio Pharma Scientist'))

st.write('You selected:', option)

# col1,col2 = st.columns([3,5])
# col3,col4= st.columns(2)
# imageLocation = col3.empty()
# imageLocation.image(img,width=480)
# if col4.checkbox("AUTO ENHANCE"):
#     imageLocation.title("K")
if option == 'OncoClinician':

    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        # st.write(string_data)



        # Can be used wherever a "file-like" object is accepted:
        st.write('You uploaded:', uploaded_file)
        if "MRD" in uploaded_file.name:
            #sdas
            data= pd.read_csv(uploaded_file)
            data =  data.dropna(axis=0)
            data=data.reset_index(drop=True)

            x = data["Time"]
            y = data["CTC count"]



            # st.subheader("Define a custom colorscale")
            # df = px.data.iris()
            fig1 = px.line(
            data,
            x="Time",
            y="CTC count",
            text="CTC count",
            # color = "Oncology Milestone",
            markers=True,
            hover_data=["Oncology Milestone"],
            # color_discrete_sequence=['red']
             color_discrete_sequence=px.colors.sequential.Inferno,
            # labels={'x':'t', 'y':'cos(t)'}
            )
            fig1.update_traces(textposition="bottom right")
            # fig.show()
            fig2 = px.scatter(data,
            x="Time",
            y="CTC count",
            # text="CTC count",
            color = "CTC count",
            hover_data=["Oncology Milestone"],
            color_continuous_scale=px.colors.sequential.Viridis)
            fig3 = go.Figure(data=fig1.data + fig2.data)

            fig3.update_layout(
            title='<b>MRD Curve</b><br><i>(Hover over the points to see the Oncology Milestones)</i>',
            # title='<span class="bold">MRD Curve</span><i>(Hover over the points to see the Oncology Milestones)</i>',
            xaxis_title = "<b>Time (in Weeks)</b>",
            yaxis_title = "<b>CTC Count (Cells/7.5 ml)</b>",
            font=dict(
                size = 18,
                
                )
            )
            st.plotly_chart(fig3, theme="streamlit", use_conatiner_width=True)
            st.write(data)
        else :
            st.write('Your uploaded File is not having MRD Data')




if option == 'Bio Pharma Scientist':
    # pyautogui.hotkey("ctrl","F5")



    placeholder.title("Survival Curve(Kaplan-Meier Plot)")

    # placeholder_ = st.empty()



    # if uploaded_file != None:
    #     del uploaded_file
    # if uploaded_file is not None:

    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        # st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        if "survival" in uploaded_file.name:
            #
            data= pd.read_csv(uploaded_file)
            data =  data.dropna(axis=0)
            data=data.reset_index(drop=True)
       

        

        
            add_selectbox = st.sidebar.selectbox(
            "Please select the type of Graph",
            ("PFS at Baseline", "PFS at 4 Weeks", "OS at Baseline","OS at 4 Weeks")
            )
            st.write('Graph type:', add_selectbox)
            # col1,col2=st.columns(2)
        
            # if st.sidebar.button("Show Whole Data")
        

            if add_selectbox == "PFS at Baseline":

                for i in range(len(data['CTCs counts at baseline'])):
                    if data['CTCs counts at baseline'][i] < 5:
                        data['CTCs counts at baseline'][i]= 1
                    elif data['CTCs counts at baseline'][i] >= 5:
                        data['CTCs counts at baseline'][i] = 2
                one = ((data["CTCs counts at baseline"] == 1 ))
                two = ((data["CTCs counts at baseline"] == 2 ))

                plt.figure(figsize=(5,5)) 
                ax = plt.subplot()
                # ax.set_figwidth(10)
                ax.set_ylabel("Probability of Survival")
                kmf1 =KaplanMeierFitter()
                kmf1.fit(durations = data[one]["PFS at baseline"], event_observed = data[one]["Status PFS"],label = "CTCs count < 5")
                kmf1.plot_survival_function(ax=ax,ci_show=False,color="blue")
                kmf2 =KaplanMeierFitter()
                kmf2.fit(durations = data[two]["PFS at baseline"], event_observed = data[two]["Status PFS"],label = "CTCs count >=5")
                kmf2.plot_survival_function(ax=ax,ci_show=False,color="red")
                from lifelines.plotting import add_at_risk_counts
                add_at_risk_counts(kmf1, kmf2)
                result = multivariate_logrank_test(data["PFS at baseline"],data["CTCs counts at baseline"],data["Status PFS"])
                plt.title("$p$-value :" + str(result.p_value))
                plt.ylabel("Progression Free Survival")
                col1,col2=st.columns(2)
                col1.pyplot(ax.get_figure())
                # st.pyplot(ax.get_figure(),width=10)
                st.write(data)

            if add_selectbox == "PFS at 4 Weeks":
                
                for i in range(len(data['CTCs counts at 4 weeks  '])):
                    if data['CTCs counts at 4 weeks  '][i] < 5:
                        data['CTCs counts at 4 weeks  '][i]= 1
                    elif data['CTCs counts at 4 weeks  '][i] >= 5:
                        data['CTCs counts at 4 weeks  '][i] = 2
                one = ((data["CTCs counts at 4 weeks  "] == 1 ))
                two = ((data["CTCs counts at 4 weeks  "] == 2 ))
                ax = plt.subplot()
                ax.set_ylabel("Probability of Survival")
                kmf1 =KaplanMeierFitter()
                kmf1.fit(durations = data[one]["PFS from weeks 4"], event_observed = data[one]["Status PFS"],label = "CTCs count < 5")
                kmf1.plot_survival_function(ax=ax,ci_show=False,color="blue")
                kmf2 =KaplanMeierFitter()
                kmf2.fit(durations = data[two]["PFS from weeks 4"], event_observed = data[two]["Status PFS"],label = "CTCs count >=5")
                kmf2.plot_survival_function(ax=ax,ci_show=False,color="red")
                from lifelines.plotting import add_at_risk_counts
                add_at_risk_counts(kmf1, kmf2)
                result = multivariate_logrank_test(data["PFS from weeks 4"],data["CTCs counts at 4 weeks  "],data["Status PFS"])
                plt.title("$p$-value :" + str(result.p_value))
                plt.ylabel("Progression Free Survival")
                col1,col2=st.columns(2)
                col1.pyplot(ax.get_figure())
                st.write(data)

            if add_selectbox == "OS at Baseline":

                for i in range(len(data['CTCs counts at baseline'])):
                    if data['CTCs counts at baseline'][i] < 5:
                        data['CTCs counts at baseline'][i]= 1
                    elif data['CTCs counts at baseline'][i] >= 5:
                        data['CTCs counts at baseline'][i] = 2
                one = ((data["CTCs counts at baseline"] == 1 ))
                two = ((data["CTCs counts at baseline"] == 2 ))
                ax = plt.subplot()
                ax.set_ylabel("Probability of Survival")
                kmf1 =KaplanMeierFitter()
                kmf1.fit(durations = data[one]["OS at baseline"], event_observed = data[one]["Status OS"],label = "CTCs count < 5")
                kmf1.plot_survival_function(ax=ax,ci_show=False,color="blue")
                kmf2 =KaplanMeierFitter()
                kmf2.fit(durations = data[two]["OS at baseline"], event_observed = data[two]["Status OS"],label = "CTCs count >=5")
                kmf2.plot_survival_function(ax=ax,ci_show=False,color="red")
                from lifelines.plotting import add_at_risk_counts
                add_at_risk_counts(kmf1, kmf2)
                result = multivariate_logrank_test(data["OS at baseline"],data["CTCs counts at baseline"],data["Status OS"])
                plt.title("$p$-value :" + str(result.p_value))
                plt.ylabel("Progression Free Survival")
                col1,col2=st.columns(2)
                col1.pyplot(ax.get_figure())

                st.write(data)
            if add_selectbox == "OS at 4 Weeks":
                
                for i in range(len(data['CTCs counts at 4 weeks  '])):
                    if data['CTCs counts at 4 weeks  '][i] < 5:
                        data['CTCs counts at 4 weeks  '][i]= 1
                    elif data['CTCs counts at 4 weeks  '][i] >= 5:
                        data['CTCs counts at 4 weeks  '][i] = 2
                one = ((data["CTCs counts at 4 weeks  "] == 1 ))
                two = ((data["CTCs counts at 4 weeks  "] == 2 ))
                ax = plt.subplot()
                ax.set_ylabel("Probability of Survival")
                kmf1 =KaplanMeierFitter()
                kmf1.fit(durations = data[one]["OS from weeks 4"], event_observed = data[one]["Status OS"],label = "CTCs count < 5")
                kmf1.plot_survival_function(ax=ax,ci_show=False,color="blue")
                kmf2 =KaplanMeierFitter()
                kmf2.fit(durations = data[two]["OS from weeks 4"], event_observed = data[two]["Status OS"],label = "CTCs count >=5")
                kmf2.plot_survival_function(ax=ax,ci_show=False,color="red")
                from lifelines.plotting import add_at_risk_counts
                add_at_risk_counts(kmf1, kmf2)
                result = multivariate_logrank_test(data["OS from weeks 4"],data["CTCs counts at 4 weeks  "],data["Status OS"])
                plt.title("$p$-value :" + str(result.p_value))
                plt.ylabel("Progression Free Survival")
                col1,col2=st.columns(2)
                col1.pyplot(ax.get_figure())
                st.write(data)
        
            df1 = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
            st.map(df1)

            df2 = pd.DataFrame(np.random.randn(20, 2) / [50, 50] + [12.9107966, 77.6760177],columns=['lat', 'lon'])
            st.map(df2)

        else :
                st.write('Your uploaded File is not having Survial Curve Data')        

if option == 'Doctor':
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        # st.write(string_data)



        # Can be used wherever a "file-like" object is accepted:
        st.write('You uploaded:', uploaded_file)
        if "Integrated" in uploaded_file.name:
            #sdas
            df= pd.read_csv(uploaded_file)
            df = df.dropna(axis=0)
            data = df[['Time', 'CTC count', 'Oncology Milestone']]
            data =  data.dropna(axis=0)
            data=data.reset_index(drop=True)

            x = data["Time"]
            y = data["CTC count"]
            data = data[['Time', 'CTC count', 'Oncology Milestone']]

            # st.subheader("Define a custom colorscale")
            # df = px.data.iris()
            fig1 = px.line(
            data,
            x="Time",
            y="CTC count",
            text="CTC count",
            # color = "Oncology Milestone",
            markers=True,
            hover_data=["Oncology Milestone"],
            # color_discrete_sequence=['red']
             color_discrete_sequence=px.colors.sequential.Inferno,
            # labels={'x':'t', 'y':'cos(t)'}
            )
            fig1.update_traces(textposition="bottom right")
            # fig.show()
            fig2 = px.scatter(data,
            x="Time",
            y="CTC count",
            # text="CTC count",
            color = "CTC count",
            hover_data=["Oncology Milestone"],
            color_continuous_scale=px.colors.sequential.Viridis)
            fig3 = go.Figure(data=fig1.data + fig2.data)

            fig3.update_layout(
            title='<b>MRD Curve</b><br><i>(Hover over the points to see the Oncology Milestones)</i>',
            # title='<span class="bold">MRD Curve</span><i>(Hover over the points to see the Oncology Milestones)</i>',
            xaxis_title = "<b>Time (in Weeks)</b>",
            yaxis_title = "<b>CTC Count (Cells/7.5 ml)</b>",
            font=dict(
                size = 18,
                
                )
            )
            st.plotly_chart(fig3, theme="streamlit", use_conatiner_width=True)
            st.write(data)

            #rbc data
            rbc_data = df[['Time', 'RBC', 'Oncology Milestone']]
            # st.subheader("Define a custom colorscale")
            # df = px.data.iris()
            x = df["Time"]
            y = df["RBC"]
            fig11 = px.line(
            rbc_data,
            x="Time",
            y="RBC",
            text="RBC",
            # color = "Oncology Milestone",
            markers=True,
            hover_data=["RBC"],
            # color_discrete_sequence=['red']
             color_discrete_sequence=px.colors.sequential.Inferno,
            # labels={'x':'t', 'y':'cos(t)'}
            )
            fig11.update_traces(textposition="bottom right")
            # fig.show()
            fig21 = px.scatter(rbc_data,
            x="Time",
            y="RBC",
            # text="CTC count",
            color = "RBC",
            hover_data=["RBC"],
            color_continuous_scale=px.colors.sequential.Viridis)
            fig31 = go.Figure(data=fig11.data + fig21.data)

            fig31.update_layout(
            #title='<b>MRD Curve</b><br><i>(Hover over the points to see the Oncology Milestones)</i>',
            # title='<span class="bold">MRD Curve</span><i>(Hover over the points to see the Oncology Milestones)</i>',
            xaxis_title = "<b>Time (in Weeks)</b>",
            yaxis_title = "<b>RBC Count (Cells/1 ml)</b>",
            font=dict(
                size = 18,
                
                )
            )
            st.plotly_chart(fig31, theme="streamlit", use_conatiner_width=True)
            st.write(rbc_data)

            #wbc count
            wbc_data = df[['Time', 'WBC', 'Oncology Milestone']]
            # st.subheader("Define a custom colorscale")
            # df = px.data.iris()
            x = df["Time"]
            y = df["WBC"]
            fig12 = px.line(
            wbc_data,
            x="Time",
            y="WBC",
            text="WBC",
            # color = "Oncology Milestone",
            markers=True,
            hover_data=["WBC"],
            # color_discrete_sequence=['red']
             color_discrete_sequence=px.colors.sequential.Inferno,
            # labels={'x':'t', 'y':'cos(t)'}
            )
            fig12.update_traces(textposition="bottom right")
            # fig.show()
            fig22 = px.scatter(wbc_data,
            x="Time",
            y="WBC",
            # text="CTC count",
            color = "WBC",
            hover_data=["WBC"],
            color_continuous_scale=px.colors.sequential.Viridis)
            fig32 = go.Figure(data=fig12.data + fig22.data)

            fig32.update_layout(
            #title='<b>MRD Curve</b><br><i>(Hover over the points to see the Oncology Milestones)</i>',
            # title='<span class="bold">MRD Curve</span><i>(Hover over the points to see the Oncology Milestones)</i>',
            xaxis_title = "<b>Time (in Weeks)</b>",
            yaxis_title = "<b>WBC Count (Cells/1 ml)</b>",
            font=dict(
                size = 18,
                
                )
            )
            st.plotly_chart(fig32, theme="streamlit", use_conatiner_width=True)
            st.write(wbc_data)

            #haemoglobin data
            hm_data = df[['Time', 'Haemoglobin', 'Oncology Milestone']]
            # st.subheader("Define a custom colorscale")
            # df = px.data.iris()
            x = df["Time"]
            y = df["Haemoglobin"]
            fig13 = px.line(
            hm_data,
            x="Time",
            y="Haemoglobin",
            text="Haemoglobin",
            # color = "Oncology Milestone",
            markers=True,
            hover_data=["Haemoglobin"],
            # color_discrete_sequence=['red']
             color_discrete_sequence=px.colors.sequential.Inferno,
            # labels={'x':'t', 'y':'cos(t)'}
            )
            fig13.update_traces(textposition="bottom right")
            # fig.show()
            fig23 = px.scatter(hm_data,
            x="Time",
            y="Haemoglobin",
            # text="CTC count",
            color = "Haemoglobin",
            hover_data=["Haemoglobin"],
            color_continuous_scale=px.colors.sequential.Viridis)
            fig33 = go.Figure(data=fig13.data + fig23.data)

            fig33.update_layout(
            #title='<b>MRD Curve</b><br><i>(Hover over the points to see the Oncology Milestones)</i>',
            # title='<span class="bold">MRD Curve</span><i>(Hover over the points to see the Oncology Milestones)</i>',
            xaxis_title = "<b>Time (in Weeks)</b>",
            yaxis_title = "<b>Haemoglobin Count (Cells/1 ml)</b>",
            font=dict(
                size = 18,
                
                )
            )
            st.plotly_chart(fig33, theme="streamlit", use_conatiner_width=True)
            st.write(hm_data)

            #LYM
            lm_data = df[['Time', 'LYM', 'Oncology Milestone']]
            # st.subheader("Define a custom colorscale")
            # df = px.data.iris()
            x = df["Time"]
            y = df["LYM"]
            fig14 = px.line(
            lm_data,
            x="Time",
            y="LYM",
            text="LYM",
            # color = "Oncology Milestone",
            markers=True,
            hover_data=["LYM"],
            # color_discrete_sequence=['red']
             color_discrete_sequence=px.colors.sequential.Inferno,
            # labels={'x':'t', 'y':'cos(t)'}
            )
            fig14.update_traces(textposition="bottom right")
            # fig.show()
            fig24 = px.scatter(lm_data,
            x="Time",
            y="LYM",
            # text="CTC count",
            color = "LYM",
            hover_data=["LYM"],
            color_continuous_scale=px.colors.sequential.Viridis)
            fig34 = go.Figure(data=fig14.data + fig24.data)

            fig34.update_layout(
            #title='<b>MRD Curve</b><br><i>(Hover over the points to see the Oncology Milestones)</i>',
            # title='<span class="bold">MRD Curve</span><i>(Hover over the points to see the Oncology Milestones)</i>',
            xaxis_title = "<b>Time (in Weeks)</b>",
            yaxis_title = "<b>LYM (Cells/1 ml)</b>",
            font=dict(
                size = 18,
                
                )
            )
            st.plotly_chart(fig34, theme="streamlit", use_conatiner_width=True)
            st.write(lm_data)

            #MN
            mon_data = df[['Time', 'MON', 'Oncology Milestone']]
            # st.subheader("Define a custom colorscale")
            # df = px.data.iris()
            x = df["Time"]
            y = df["MON"]
            fig15 = px.line(
            mon_data,
            x="Time",
            y="MON",
            text="MON",
            # color = "Oncology Milestone",
            markers=True,
            hover_data=["MON"],
            # color_discrete_sequence=['red']
             color_discrete_sequence=px.colors.sequential.Inferno,
            # labels={'x':'t', 'y':'cos(t)'}
            )
            fig15.update_traces(textposition="bottom right")
            # fig.show()
            fig25 = px.scatter(mon_data,
            x="Time",
            y="MON",
            # text="CTC count",
            color = "MON",
            hover_data=["MON"],
            color_continuous_scale=px.colors.sequential.Viridis)
            fig35 = go.Figure(data=fig15.data + fig25.data)

            fig35.update_layout(
            #title='<b>MRD Curve</b><br><i>(Hover over the points to see the Oncology Milestones)</i>',
            # title='<span class="bold">MRD Curve</span><i>(Hover over the points to see the Oncology Milestones)</i>',
            xaxis_title = "<b>Time (in Weeks)</b>",
            yaxis_title = "<b>MON (Cells/1 ml)</b>",
            font=dict(
                size = 18,
                
                )
            )
            st.plotly_chart(fig35, theme="streamlit", use_conatiner_width=True)
            st.write(mon_data)


            #radiologydata
            image1 = Image.open('radiologicalImages/'+df['Radiology Image'].head(1).values[0])
            st.image(image1, caption='Radiology Image')

            #histologydata
            image2 = Image.open('pathologicalImages/'+df['Pathology Image'].head(1).values[0])
            st.image(image2, caption='Pathology Image')
        else :
            st.write('Your uploaded File is not having Integrated Data')