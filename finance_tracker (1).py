import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv("c:\\Users\\HP\\Downloads\\UK_Student_Expenses.csv")

st.title("	:chart_with_upwards_trend: Finance Tracker")

st.sidebar.header("Enter data:")
gender_options = ['Male', 'Female']
selected_gender = st.sidebar.selectbox("Select Gender:", gender_options)
edu_options = ['Diploma', 'Undergraduate', 'Graduate', 'Postgraduate']
selected_edu = st.sidebar.selectbox("Select Level of Education:", edu_options)
monthly_income = st.sidebar.number_input("Enter Monthly Income:", min_value=0, step=100)

df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
df['Level_of_Education'] = df['Level_of_Education'].map({'Diploma': 0, 'Undergraduate': 1, 'Graduate': 2, 'Post graduate': 3})

data1 = df[['Level_of_Education', 'Gender', 'Monthly_Income', 'Total Monthly Expense']]
X = data1.drop('Total Monthly Expense', axis=1)
y = data1['Total Monthly Expense']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

if selected_gender == 'Male':
    selected_gender_ip = 0
elif selected_gender == 'Female':
    selected_gender_ip = 1

if selected_edu == 'Diploma':
    selected_edu_ip = 0
elif selected_edu == 'Undergraduate':
    selected_edu_ip = 1
elif selected_edu == 'Graduate':
    selected_edu_ip = 2
elif selected_edu == 'Postgraduate':
    selected_edu_ip = 3

user_input = pd.DataFrame({
    'Gender': [selected_gender_ip],
    'Level_of_Education': [selected_edu_ip],
    'Monthly_Income': [monthly_income]
})

user_input = user_input[X_train.columns]

if st.sidebar.button("Submit"):
    predicted_expense = model.predict(user_input)
    predicted_expense_format = "{:.2f}".format(predicted_expense[0])
    st.sidebar.subheader("Predicted Total Monthly Expense:")
    st.sidebar.write(predicted_expense_format)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("Total Number of People")
    total_people = df.shape[0]
    st.title(total_people)

with col2:
    st.write("Average Age")
    average_age = df['Age'].mean()
    st.title(f"{average_age:.0f}")

with col3:
    st.write("Average Monthly Income")
    average_income = df['Monthly_Income'].mean()
    st.title(f"{average_income:.2f}")

with col4:
    st.write("Average Expenses")
    average_monthly_expense = df['Total Monthly Expense'].mean()
    st.title(f"{average_monthly_expense:.2f}")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(df,x = "Level_of_Education", y = "Total Monthly Expense",title="Monthly expenses vs Level of education", template = "seaborn", height=400)
    st.plotly_chart(fig,use_container_width=True)

with col2:
    merged_data = df.groupby('Monthly_Income')['Total Monthly Expense'].mean().reset_index()

    fig = px.line(merged_data, x='Monthly_Income', y='Total Monthly Expense',
                labels={'Monthly_Income': 'Monthly Income', 'Total Monthly Expense': 'Avg Monthly Expense'}, title="Average Monthly Expenses vs Monthly Income",height=400)
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    gender_ratio = df['Gender'].value_counts(normalize=True)
    fig2 = px.pie(names=gender_ratio.index, values=gender_ratio.values, title='Male to Female Ratio')
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    edu_counts = df['Level_of_Education'].value_counts()
    fig3 = px.pie(names=edu_counts.index, values=edu_counts.values, title='Distribution of Education Levels')
    st.plotly_chart(fig3, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    age_counts = df['Age'].value_counts()
    fig1 = px.bar(x=age_counts.index, y=age_counts.values, labels={'x': 'Age', 'y': 'Number of People'}, title="Number of People by Age", height=350)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    edu_counts = df['Level_of_Education'].value_counts()
    fig3 = px.bar(x=edu_counts.index, y=edu_counts.values, labels={'x': 'Education Level', 'y': 'Number of People'}, title="Number of People by Level of Education", height=350)
    st.plotly_chart(fig3, use_container_width=True)

with col3:
    fig3 = px.histogram(df, x="Monthly_Income", title="Number of People for Each Monthly Income", height=350)
    st.plotly_chart(fig3, use_container_width=True)
