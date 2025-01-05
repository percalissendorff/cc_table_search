# mla_tablewords.py
########################
# Description:
"""
	Script to read and examine .odt files similar to word-documents
	containing tables, flagging multiple of the same entries as answers.
	"""
	
# ---------------------------------------------------------------------
# Load modules
import numpy as np
import pandas as pd
import pypdfium2 as pdfium
import docx
import sys
import read_functions
import streamlit as st
from streamlit import session_state
# ---------------------------------------------------------------------
# Define files

#fname = '/home/per/Dropbox/Blandat/test_document_for_pancakedevil_onecol.odt'
uploaded_file = st.file_uploader("Upload your table here, should be .odt file for now.", type='odt', accept_multiple_files=False, key="up1")

if uploaded_file is not None:
	# Read file
	if ".docx" in uploaded_file:
		df = read_functions.read_docx(uploaded_file)
	elif ".odt" in uploaded_file:
		print("This is a print statemetn")
		st.write("We made it this far")
		df = pd.read_excel(uploaded_file, header=None)
	elif ".pdf" in uploaded_file:
		df = read_functions.read_pdf(uploaded_file)
	else:
		print("Unknown data format for input data table. Try Word (.docx) or OpenOffice (.odt).")

	
	#df = pd.read_excel(uploaded_file, header=None)
	#st.dataframe(df)

########################################################################
st.write("I am not in the if-loop")
print("This print is outside the if-loop")




