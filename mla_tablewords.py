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

fname = uploaded_file.name
st.write("Uploaded file: "+fname)

if uploaded_file is not None:
	# Read file
	if ".docx" in fname:
		df = read_functions.read_docx(uploaded_file)
	elif ".odt" in fname:
		st.write("We made it this far")
		df = pd.read_excel(uploaded_file, header=None)
	elif ".pdf" in fname:
		df = read_functions.read_pdf(uploaded_file)
	else:
		st.write("Unknown data format for input data table. Try Word (.docx) or OpenOffice (.odt).")

	
	#df = pd.read_excel(uploaded_file, header=None)
	#st.dataframe(df)

########################################################################
# Collect all ID numbers and answers
answers = read_functions.search_words(df)


# Question IDs
qids = list(answers.keys())

# Make exceptions. Could import a list from separate docutment instead
exception_file = st.file_uploader("Upload your exceptions here, should be .txt file containing a list for now.", type='txt', accept_multiple_files=False, key="up2")
if uploaded_file is not None:
	with open(exception_file, 'r') as f:
		exceps = [line.strip() for line in f]
else:
	with open('default_exceptions.dat', 'r') as f:
		exceps = [line.strip() for line in f]


# Save flagged words and id
flagged_word = []
flagged_id = []
flagged = {}

# Step through all answers starting with first
for i in range(0, len(qids)-1):
	qid = qids[i]
	split_answer = (" ".join(answers[qid])).split()
	
	for j in range(0, len(split_answer)):		# Step through words in answer
		current_word = split_answer[j]
		
		for k in range(i+1, len(qids)):		# Step through other answers
			# question ids
			oqid = qids[k]		# other question ids
			other_answers = (" ".join(answers[oqid])).split()
			if current_word in other_answers:	# Find current word in other answers
				# Ignore exceptions and shorter words
				if current_word in exceps or len(current_word) < 3:
					pass
				else:							# Save multiple instances of word in answer
					flagged_word.append(current_word)
					flagged_id.append([qid, oqid])
					
					# Check if flagged word exists, otherwise create dictionary key
					# and add matching word ID to key
					if current_word not in flagged:
						flagged.setdefault(current_word, []).append(qid)
						flagged.setdefault(current_word, []).append(oqid)
					# If word exists and is flagged, only add the following matching ID to key
					else:
						# Do not add the same ID several times for the same matching word
						if oqid in flagged[current_word]:
							pass
						else:
							flagged.setdefault(current_word, []).append(oqid)



# Display the results
for key, val in flagged.items():
	st.write(key, ":", val)





