import streamlit as st
import pandas as pd
import plotly.express as px

# Setting the page configuration
st.set_page_config(
    page_title="Health Data Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load data set
def load_data(csv_path):
    return pd.read_csv(csv_path)

# Loading the datasets
df = load_data('Diabetes_cleaned_data.csv')
df_importances_heart = load_data('importances.csv')
df_importances_diabetes = load_data('diabetes_importances.csv')

# Define plotting functions
def plot_condition_count_by_region(df, condition_column, title, bar_color):
    # Filter the dataframe for instances where the condition is present
    df_condition = df[df[condition_column] == 1]

    # Calculate the count of cases by region and reset the index for plotting
    condition_counts = df_condition['Region'].value_counts().reset_index()
    condition_counts.columns = ['Region', 'Count']

    # Create a bar chart using Plotly Express
    fig = px.bar(condition_counts,
                 x='Region',
                 y='Count',
                 labels={'Count': f'Number of People with {title}', 'Region': 'Region'},
                 title=f'Number of People with {title} by Region',
                 color_discrete_sequence=[bar_color])

    # Update the chart layout for better presentation
    fig.update_layout(xaxis_title="Region", yaxis_title="Number of People")

    return fig

# Create an interactive scatterplot
def scatter_plot(df, x_var, y_var):
    fig = px.scatter(df, x=x_var, y=y_var,
                     labels={x_var: x_var, y_var: y_var},
                     title=f"{y_var} vs {x_var}")
    fig.update_layout(transition_duration=500)
    return fig

def plot_feature_importance_tree(df_importances, title, color_scale):
    df_importances = df_importances.sort_values(by='Importance', ascending=False)
    fig = px.treemap(df_importances, path=['Feature'], values='Importance',
                     title=title, color='Importance', color_continuous_scale=color_scale)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

# Sidebar configuration
with st.sidebar:
    st.title('Dashboard filters 🏥')
    year_list = df['Year'].unique()
    year_list.sort()
    selected_years = st.multiselect('Select Year(s)', options=year_list, default=year_list)

    region_list = df['Region'].unique()
    selected_regions = st.multiselect('Select Region(s)', options=region_list, default=region_list)


    ethnicity_list = df['Region'].unique()
    selected_ethnicity = st.multiselect('Select Ethnicity(s)', options=ethnicity_list, default=ethnicity_list)

    gender_list = df['Gender'].unique()
    selected_genders = st.multiselect('Select Gender', options=gender_list, default=gender_list)

    # variables for the scatter plot
    continuous_vars = ['Age', 'BMI', 'Systolic_BP', 'Diastolic_BP', 'Cholesterol_Level(mg/dL)', 'Smoking_Per_Week', 'Alcohol_Consumption_Per_Week']
    x_variable = st.selectbox("Choose X-axis variable:", continuous_vars, index=1)  # Default to BMI
    y_variable = st.selectbox("Choose Y-axis variable:", continuous_vars, index=4)  # Default to Cholesterol_Level

# Filter data based on selections
filtered_data = df[(df['Year'].isin(selected_years)) &
                   (df['Region'].isin(selected_regions)) &
                   (df['Gender'].isin(selected_genders))]

# Main panel setup
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.subheader('Heart Disease Analysis')
    fig1 = plot_condition_count_by_region(filtered_data, 'Heart_Disease', 'Heart Disease', 'red')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader('Feature Importance for Heart Disease')
    fig4 = plot_feature_importance_tree(df_importances_heart, 'Feature Importances for Heart Disease', 'Reds')
    st.plotly_chart(fig4, use_container_width=True)



with col2:
    st.subheader('Diabetes Analysis')
    fig2 = plot_condition_count_by_region(filtered_data, 'Diabetes', 'Diabetes', 'Blue')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader('Feature Importance for Diabetes')
    fig5 = plot_feature_importance_tree(df_importances_diabetes, 'Feature Importances for Diabetes', 'Blues')
    st.plotly_chart(fig5, use_container_width=True)

# Displaying the flexible scatter plot
st.title('Interactive Scatter Plot Analysis')
fig_flexible = scatter_plot(df, x_variable, y_variable)
st.plotly_chart(fig_flexible, use_container_width=True)

# Displaying the line graph image
st.title('Projected Average Smoking and Alcohol Consumption (2024)')
st.image('Picture 1.png', caption='Projected Average Smoking and Alcohol Consumption for 2024')