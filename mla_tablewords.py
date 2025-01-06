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
# Initiating user friendly stuff
st.title("Table search multiples")




# ---------------------------------------------------------------------

# Define files
st.subheader("Input table")
st.write("Input table should be a single column, formatted to have one row for question id, one row for the question, followed by a number of rows corresponding to answers.")
st.write("The ID row should have the phrase 'ID' in it.")
st.write("The question row should have the word 'Question' in it.")
st.write("The answer rows should be numbered, with right paranthesis after the numbers, as 1), 2), 3) and 4).")
st.write("The code is case insensitive, and will flag the same word regardless if it is in caps or lower case letters.")
st.write("The current version of the code should be able to handle Word (.docx), open office (.odt), and PDF (.pdf) files.")

st.write("An example of how a table may look like is presented below, followed by a description of the code output.")

st.image("table_example.png", width=400, caption="Example input table structure. In this example, the code will flag the word [Grey], as it appears in both questions. The code will NOT identify the word [color] and [colour] as multiples, because of their different spelling.")



uploaded_file = st.file_uploader("Upload your table here.", type=['odt', 'docx', 'pdf'], accept_multiple_files=False, key="up1")

fname = uploaded_file.name
st.write("Uploaded file: "+fname)

if uploaded_file is not None:
	# Read file
	if ".docx" in fname:
		df = read_functions.read_docx(uploaded_file)
	elif ".odt" in fname:
		df = pd.read_excel(uploaded_file, header=None)
	elif ".pdf" in fname:
		df = read_functions.read_pdf(uploaded_file)
	else:
		st.write("Unknown data format for input data table. Try Word (.docx) or OpenOffice (.odt).")

########################################################################
# Collect all ID numbers and answers
answers = read_functions.search_words(df)

# Question IDs
qids = list(answers.keys())

# Make exceptions. Could import a list from separate docutment instead
st.subheader("Exceptions")
st.write("Below you can upload a text file containing words that should be excepted from the search. If you do not have one, you can just leave the upload empty and the code will take a default list of common words, such as prepositions, and ignore them for the multiple instance search.")
st.write("The exception list should be either .txt or .dat format, and the structure can be a single column of words.")
st.write("The current version is not smart, and does not recognise different grammatical uses or pluralisations of the same word. You will need to add all instances of the word")

exception_file = st.file_uploader("Upload your list of exceptions here.", type=['txt', 'dat'], accept_multiple_files=False, key="up2")

if exception_file:
	ename = exception_file.name
	st.write("Uploaded exception file: ", ename)
	
	# Read the file as bytes
	file_contents = exception_file.read()

	# If you need to handle the 'b' character:
	if file_contents.startswith(b'\xef\xbb\xbf'):
		file_contents = file_contents[3:]  # Remove BOM

	# Decode the bytes to string (assuming UTF-8 encoding)
	exceps = file_contents.decode("utf-8")
	st.write("exceptions: ")

else:		# Read defualt list of exceptions
	st.write("Using default exceptions: ")
	with open("default_exceptions.dat", 'r') as f:
		exceps = f.read()

st.write(exceps)

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
st.subheader("Flagged words and corresponding question IDs: ")
for key, val in flagged.items():
	st.write(key, ":", val)





