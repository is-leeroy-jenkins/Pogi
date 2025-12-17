'''
	# ******************************************************************************************
	#  Assembly:                Pogi
	#  Filename:                app.py
	#  Author:                  Terry D. Eppler (derived)
	#  Created:                 2025-12-16
	#
	#  Purpose:
	#  --------
	#  Streamlit application wrapper for the Pogi ML notebook (models.ipynb).
	#  Enables interactive data upload, preprocessing, model training,
	#  and diagnostics for SF-133 / Treasury Account Symbol forecasting.
	# ******************************************************************************************
'''

from __future__ import annotations

import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
	r2_score,
	mean_squared_error,
	accuracy_score,
	confusion_matrix,
	classification_report,
)

from sklearn.linear_model import (
	LinearRegression,
	Ridge,
	Lasso,
	ElasticNet,
	LogisticRegression,
	Perceptron,
)
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.neural_network import MLPRegressor, MLPClassifier

import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------------------------------------------
# Streamlit Configuration
# --------------------------------------------------------------------------------------

st.set_page_config(
	page_title='Pogi — Budget Execution',
	layout='wide',
)

st.title( '🏛️ Pogi — Outlay Projections' )
st.markdown(
	"""
	### **Machine-learning modeling and diagnostics for SF-133 / TAS-Level Balances**
	Regression and classification pipelines derived directly from the original notebook.
	"""
)

# --------------------------------------------------------------------------------------
# Sidebar — Data Input
# --------------------------------------------------------------------------------------

st.sidebar.header( '📁 Data Input' )

uploaded_file = st.sidebar.file_uploader(
	'Upload CSV or Excel File',
	type=[ 'csv',  'xlsx' ],
)

if uploaded_file is None:
	st.info( 'Upload a dataset.' )
	st.stop( )

# --------------------------------------------------------------------------------------
# Load Data
# --------------------------------------------------------------------------------------

if uploaded_file.name.endswith( '.csv' ):
	df = pd.read_csv( uploaded_file )
else:
	df = pd.read_excel( uploaded_file )

st.subheader( '📊 Raw Dataset Preview' )
st.dataframe( df.head( ) )

# --------------------------------------------------------------------------------------
# Target Selection
# --------------------------------------------------------------------------------------

st.sidebar.header( '🎯 Target Selection' )

target_column = st.sidebar.selectbox(
	'Select Target Variable',
	options=df.columns,
)

feature_columns = st.sidebar.multiselect(
	'Select Feature Columns',
	options=[ c for c in df.columns if c != target_column ],
)

if not feature_columns:
	st.warning( 'Select at least one feature column.' )
	st.stop( )

X = df[ feature_columns ]
y = df[ target_column ]

# --------------------------------------------------------------------------------------
# Task Type
# --------------------------------------------------------------------------------------

task_type = st.sidebar.radio(
	'Modeling Task',
	[ 'Regression',
	  'Classification' ],
)

# --------------------------------------------------------------------------------------
# Preprocessing
# --------------------------------------------------------------------------------------

st.sidebar.header( '🧮 Preprocessing' )

imputer_type = st.sidebar.selectbox(
	'Missing Value Imputation',
	[ 'Simple (mean)',
	  'KNN' ],
)

scaler_type = st.sidebar.selectbox(
	'Feature Scaling',
	[ 'StandardScaler',
	  'MinMaxScaler',
	  'RobustScaler',
	  'None' ],
)

if imputer_type == 'Simple (mean)':
	imputer = SimpleImputer( strategy='mean' )
else:
	imputer = KNNImputer( )

if scaler_type == 'StandardScaler':
	scaler = StandardScaler( )
elif scaler_type == 'MinMaxScaler':
	scaler = MinMaxScaler( )
elif scaler_type == 'RobustScaler':
	scaler = RobustScaler( )
else:
	scaler = None

# --------------------------------------------------------------------------------------
# Model Selection
# --------------------------------------------------------------------------------------

st.sidebar.header( '🤖 Model' )

if task_type == 'Regression':
	model_name = st.sidebar.selectbox(
		'Select Regression Model',
		[
				'LinearRegression',
				'Ridge',
				'Lasso',
				'ElasticNet',
				'DecisionTree',
				'RandomForest',
				'SVR',
				'KNN',
				'MLP',
		],
	)
	
	model_map = {
			'LinearRegression': LinearRegression( ),
			'Ridge': Ridge( ),
			'Lasso': Lasso( ),
			'ElasticNet': ElasticNet( ),
			'DecisionTree': DecisionTreeRegressor( ),
			'RandomForest': RandomForestRegressor( ),
			'SVR': SVR( ),
			'KNN': KNeighborsRegressor( ),
			'MLP': MLPRegressor( max_iter=500 ),
	}

else:
	model_name = st.sidebar.selectbox(
		'Select Classification Model',
		[
				'LogisticRegression',
				'Perceptron',
				'DecisionTree',
				'RandomForest',
				'SVC',
				'KNN',
				'MLP',
		],
	)
	
	model_map = \
	{
		'LogisticRegression': LogisticRegression( max_iter=500 ),
		'Perceptron': Perceptron( ),
		'DecisionTree': DecisionTreeClassifier( ),
		'RandomForest': RandomForestClassifier( ),
		'SVC': SVC( ),
		'KNN': KNeighborsClassifier( ),
		'MLP': MLPClassifier( max_iter=500 ),
	}

model = model_map[ model_name ]

# --------------------------------------------------------------------------------------
# Pipeline Assembly
# --------------------------------------------------------------------------------------

steps = [ ('imputer', imputer) ]

if scaler is not None:
	steps.append( ('scaler', scaler) )

steps.append( ('model', model) )

pipeline = Pipeline( steps )

# --------------------------------------------------------------------------------------
# Train / Test Split
# --------------------------------------------------------------------------------------

test_size = st.sidebar.slider( 'Test Size', 0.1, 0.5, 0.2 )

X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=test_size, random_state=42 )

# --------------------------------------------------------------------------------------
# Train Model
# --------------------------------------------------------------------------------------

if st.sidebar.button( '🚀 Train Model' ):
	pipeline.fit( X_train, y_train )
	y_pred = pipeline.predict( X_test )
	
	st.subheader( '📈 Model Results' )
	
	if task_type == 'Regression':
		r2 = r2_score( y_test, y_pred )
		rmse = mean_squared_error( y_test, y_pred, squared=False )
		
		col1, col2 = st.columns( 2 )
		col1.metric( 'R²', f'{r2:.4f}' )
		col2.metric( 'RMSE', f'{rmse:.4f}' )
		
		fig, ax = plt.subplots( )
		ax.scatter( y_test, y_pred )
		ax.set_xlabel( 'Actual' )
		ax.set_ylabel( 'Predicted' )
		ax.set_title( 'Actual vs Predicted' )
		st.pyplot( fig )
	
	else:
		acc = accuracy_score( y_test, y_pred )
		st.metric( 'Accuracy', f'{acc:.4f}' )
		
		st.text( 'Classification Report' )
		st.text( classification_report( y_test, y_pred ) )
		
		cm = confusion_matrix( y_test, y_pred )
		fig, ax = plt.subplots( )
		sns.heatmap( cm, annot=True, fmt='d', ax=ax )
		ax.set_title( 'Confusion Matrix' )
		st.pyplot( fig )

# --------------------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------------------

st.markdown( '---' )
st.caption( 'Budget Execution & Machine Learning | Streamlit Application' )
