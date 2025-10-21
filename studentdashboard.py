import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from fpdf import FPDF
#load dataset
sdata = pd.read_csv("data/student_exam_scores.csv")
#streamlit
st.title("🧑‍🎓Students Examination Performance")
st.subheader("Analytical Summary")
st.markdown(""" Overall the students have performed better in their past exams as compared to the finals.
Despite more study hours that students have dedicated for their final exams.
""")
#table to summarize scores by scores, hours studied
st.write("Summary of Top 10 Students Performance according to scores and their hours of study")
table = sdata.head(10)[['previous_scores','exam_score','hours_studied']]
st.dataframe(table)
#fxns to handle reports (PDF)
def createhist(sdata):
    fig = px.histogram(sdata, x='exam_score', nbins=10, title='Student Exam Performance')
    fig.update_layout(
        width=700,
        height=400,
        barmode='group',
        bargap=0.1,
        plot_bgcolor='white',
    )
    return  fig
def previousbar(sdata):
    topscores = sdata['previous_scores'].value_counts().head(5).reset_index()
    topscores.columns = ['Previous_scores', 'Students']
    fig = px.bar(topscores, x='Students', y='Previous_scores', orientation='h',
                       title='Previous Student Exam Performance', color='Students',
                       color_discrete_sequence=px.colors.sequential.Blues,
                       )
    fig.update_layout(
        width=600,
        height=400,
        plot_bgcolor='white',
    )
    return fig
def currentbar(sdata):
    currtopscores = sdata['exam_score'].value_counts().head(5).reset_index()
    currtopscores.columns = ['Exam_scores', 'Students']
    fig = px.bar(currtopscores, x='Students', y='Exam_scores', orientation='h',
                              title='Current Student Exam Performance', color='Students',
                              color_discrete_sequence=px.colors.sequential.Blues,
                              )
    fig.update_layout(
        width=600,
        height=400,
        plot_bgcolor='white',
    )
    return fig
def heatmapfig(sdata):
    corr = sdata[['hours_studied', 'sleep_hours', 'attendance_percent', 'previous_scores', 'exam_score']].corr()
    fig = px.imshow(corr, text_auto='.3f', color_continuous_scale='Viridis', title='Correlation Heatmap',
                         aspect='auto')
    fig.update_layout(
        width=600,
        height=400,
    )
    return fig
def piechart(sdata):
    pavg = sdata['previous_scores'].mean()
    avg = sdata['exam_score'].mean()
    fig = px.pie(names=['Previous Scores', 'Exam Score'],
                     values=[pavg, avg],
                     title='Results Comparison',
                     color_discrete_sequence=['#66b3ff', '#ff9999'])
    return fig
def regressionfig(sdata):
    x = sdata['hours_studied']
    y = sdata['exam_score']
    # fit our regression line since plotly doesnot automatically understands regression plots like seaborn
    coeffs = np.polyfit(x, y, 1)
    reg_line = np.poly1d(coeffs)
    x_range = np.linspace(x.min(), x.max(), 20)
    ypred = reg_line(x_range)
    # create the visual
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=ypred, mode='markers', name='Hours studied'))
    fig.add_trace(go.Scatter(x=x_range, y=ypred, mode='lines', name='Exam Score'))
    fig.update_layout(
        width=600,
        height=400,
        font=dict(size=10),
        plot_bgcolor='white',
        title='How the number of hours studied relate with the student exam scores',
        xaxis_title='Hours Studied',
        yaxis_title='Exam Score',
    )
    return fig
#histplot
hist_fig = px.histogram(sdata,x='exam_score', nbins=10, title='Student Exam Performance')
hist_fig.update_layout(
    width=700,
    height=400,
    barmode='group',
    bargap=0.1,
    plot_bgcolor='white',
)
st.plotly_chart(hist_fig, use_container_width=True)
#topscorers (Previous results)
topscores = sdata['previous_scores'].value_counts().head(5).reset_index()
topscores.columns = ['Previous_scores','Students']
score_fig = px.bar(topscores,x='Students',y='Previous_scores',orientation='h',
                   title='Previous Student Exam Performance',color='Students',
                   color_discrete_sequence=px.colors.sequential.Blues,
                  )
score_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
)
st.plotly_chart(score_fig, use_container_width=True)
#topscorers current results
currtopscores = sdata['exam_score'].value_counts().head(5).reset_index()
currtopscores.columns = ['Exam_scores','Students']
currentscore_fig = px.bar(currtopscores,x='Students',y='Exam_scores',orientation='h',
                   title='Current Student Exam Performance',color='Students',
                   color_discrete_sequence=px.colors.sequential.Blues,
                  )
currentscore_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
)
st.plotly_chart(currentscore_fig, use_container_width=True)
#heatmap correlation
corr = sdata[['hours_studied','sleep_hours','attendance_percent','previous_scores','exam_score']].corr()
heat_fig = px.imshow(corr, text_auto='.3f', color_continuous_scale='Viridis',title='Correlation Heatmap',aspect='auto')
heat_fig.update_layout(
    width=600,
    height=400,
)
st.plotly_chart(heat_fig, use_container_width=True)
#pie chart visual to compare btn the 2 average scores
pavg = sdata['previous_scores'].mean()
avg = sdata['exam_score'].mean()
pie_fig = px.pie(names=['Previous Scores','Exam Score'],
                 values= [pavg,avg],
                 title = 'Results Comparison',
                 color_discrete_sequence=['#66b3ff', '#ff9999'])
st.plotly_chart(pie_fig, use_container_width=True)
st.markdown(f"📌 **Average Previous Score:** {pavg:.2f} | **Final Exam Score:** {avg:.2f}")
#regplot visual to show correlation btn attendace percent and previous scores
x= sdata['hours_studied']
y = sdata['exam_score']
#fit our regression line since plotly doesnot automatically understands regression plots like seaborn
coeffs = np.polyfit(x,y,1)
reg_line = np.poly1d(coeffs)
x_range = np.linspace(x.min(),x.max(),20)
ypred = reg_line(x_range)
#create the visual
reg_fig = go.Figure()
reg_fig.add_trace(go.Scatter(x=x, y=ypred, mode='markers', name='Hours studied'))
reg_fig.add_trace(go.Scatter(x=x_range, y=ypred, mode='lines', name='Exam Score'))
reg_fig.update_layout(
    width=600,
    height=400,
    font=dict(size=10),
    plot_bgcolor='white',
    title='How the number of hours studied relate with the student exam scores',
    xaxis_title='Hours Studied',
    yaxis_title='Exam Score',
)
st.plotly_chart(reg_fig, use_container_width=True)
#streamlit - layout
chart_option = st.selectbox( "Choose a chart to download",
     ['📊Histogram','🥧Pie Chart','⏸️Previous Bar Chart','⏸️Current Bar Chart','📈Scatter Plot','🌡️Heat Map'])
if chart_option == '🥧Pie Chart':
        selected_fig = pie_fig
elif chart_option == '📊Histogram':
    selected_fig = hist_fig
elif chart_option == '⏸️Previous Bar Chart':
    selected_fig = score_fig
elif chart_option == '⏸️Current Bar Chart':
    selected_fig = currentscore_fig
elif chart_option == '📈Scatter Plot':
    selected_fig = reg_fig
elif chart_option == '🌡️Heat Map':
    selected_fig = heat_fig
else:
    selected_fig = None
if selected_fig:
    st.download_button("Download Chart as HTML", selected_fig.to_html(), file_name="chart.html")
if st.button("Download Full Report"):
    with st.spinner("Downloading Full Report"):
        #call the fxns
        createhist(sdata).write_image("histogram.png")
        previousbar(sdata).write_image("previousbar.png")
        currentbar(sdata).write_image("currentbar.png")
        heatmapfig(sdata).write_image("heatmap.png")
        piechart(sdata).write_image("piechart.png")
        regressionfig(sdata).write_image("regression.png")
        #create pdf
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for img in [
            "histogram.png", "previousbar.png", "currentbar.png",
             "heatmap.png","piechart.png","regression.png"]:
            pdf.image(img,x=10,w=180)
        pdf.output("report.pdf")




