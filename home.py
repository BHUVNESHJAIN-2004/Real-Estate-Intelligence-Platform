import streamlit as st

st.set_page_config(
    page_title="Property Recommandation App",
    # page_icon="",
)

st.write("""

# 🏠 Real Estate Intelligence Platform

### Transforming Property Search with Machine Learning and Data Analytics

Welcome to the Real Estate Intelligence Platform, an end-to-end machine learning solution designed to help buyers, investors, and real estate enthusiasts make informed property decisions through predictive analytics, market insights, and intelligent recommendations.

---

## 🚀 Project Overview

This platform combines Real Estate Data Collection, Machine Learning, Data Analytics, and Recommendation Systems to provide users with comprehensive property insights.

The application analyzes thousands of property records collected from different sectors and localities of the city. Using this information, it predicts property prices, generates analytical insights, and recommends similar properties based on user preferences.

Whether you are looking to buy a property, compare localities, analyze market trends, or discover similar properties, this platform provides data-driven solutions to support better decision-making.

---

## 📊 Modules Available

### 🔹 Property Price Prediction

The Price Prediction module uses machine learning algorithms trained on historical property data to estimate the market value of a property.

Users can provide:

• Property Sector / Locality
• Property Type
• Area (Sq. Ft.)
• Number of Bedrooms
• Number of Bathrooms
• Property Age
• Additional Property Features

Based on these inputs, the model predicts an estimated property price using learned market patterns.

---

### 🔹 Real Estate Analytics Dashboard

The Analytics module provides detailed visualizations and insights about the city's real estate market.

Key analytics include:

• Sector-wise Property Distribution
• Price Distribution Analysis
• BHK Distribution Analysis
• Average Property Prices by Sector
• Price Per Square Foot Analysis
• Feature Frequency Analysis
• Comparative Market Trends
• Locality-Level Insights

These visualizations help users understand market behavior and identify potential investment opportunities.

---

### 🔹 Smart Property Recommendation System

The Recommendation System helps users discover properties similar to a selected property.

The recommendation engine evaluates multiple factors such as:

• Location Similarity
• Property Features
• Property Configuration
• Area Specifications
• Pricing Patterns

Using similarity-based algorithms, the system recommends properties that closely match user requirements and preferences.

---

## 🧠 Machine Learning Workflow

The project follows a complete Machine Learning lifecycle:

### Data Collection

Property information is collected and aggregated from real estate sources.

### Data Cleaning

Missing values, duplicate entries, inconsistent records, and outliers are processed to improve data quality.

### Feature Engineering

Relevant features are transformed and encoded to improve model performance.

### Model Training

Machine Learning algorithms learn relationships between property attributes and market prices.

### Model Evaluation

Models are evaluated using performance metrics to ensure reliable predictions.

### Deployment

The final models are deployed through an interactive Streamlit web application.

---

## 📍 Sector-Based Market Intelligence

The platform divides the city into sectors and localities to provide location-specific analysis.

Users can:

• Compare different sectors
• Analyze average property prices
• Study market trends
• Explore property feature distributions
• Identify emerging investment locations

This enables more informed decisions compared to relying solely on city-wide averages.

---

## 🎯 Why Use This Platform?

✅ Accurate Property Price Prediction

✅ Data-Driven Decision Making

✅ Sector-Level Market Insights

✅ Intelligent Property Recommendations

✅ Interactive Visual Analytics

✅ User-Friendly Interface

✅ End-to-End Machine Learning Integration

---

## 🔍 How to Use

### Step 1

Navigate to the Price Prediction module and enter property details.

### Step 2

Generate an estimated market valuation for the property.

### Step 3

Explore the Analytics Dashboard to understand market trends and locality performance.

### Step 4

Use the Recommendation System to discover properties similar to your preferred choice.

### Step 5

Compare options and make informed real estate decisions.

---

## 🛠️ Technologies Used

• Python

• Streamlit

• Pandas

• NumPy

• Scikit-Learn

• Plotly

• Machine Learning Models

• Recommendation Systems

• Data Visualization Techniques

---

### Empowering Smarter Real Estate Decisions Through Machine Learning, Analytics, and Intelligent Recommendations.

""")


st.sidebar.success("Select a demo above.")