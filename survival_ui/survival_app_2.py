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
    ('OncoClinician','Patient', 'Bio Pharma Scientist'))

st.write('You selected:', option)

# col1,col2 = st.columns([3,5])
# col3,col4= st.columns(2)
# imageLocation = col3.empty()
# imageLocation.image(img,width=480)
# if col4.checkbox("AUTO ENHANCE"):
#     imageLocation.title("K")
if option == 'OncoClinician' or option =='Patient':

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
