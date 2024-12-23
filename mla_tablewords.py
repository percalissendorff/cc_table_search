# mla_tablewords.py
########################
# Description:
"""
	Script to read and examine .odt files similar to word-documents
	containing tables, flagging multiple of the same entries as answers.
	"""
	
# ---------------------------------------------------------------------
# Load modules
import pandas as pd
import sys
import streamlit as st
from streamlit import session_state
# ---------------------------------------------------------------------
# Define files

#fname = '/home/per/Dropbox/Blandat/test_document_for_pancakedevil_onecol.odt'
fname = st.file_uploader("Upload your table here, should be .odf file for now.", type='odf', accept_multiple_files=False, key="up1")


df = pd.read_excel(fname, engine='odf', header=None)

# Make dictionary 
def search_answers(df):
	Q = {}
	for index, row in df.iterrows():
		# Step through rows in table
		# ~ answers = []
		for column in df.columns:
			value = str(row[column])
			# Save ID
			if "ID" in value:
				current_ID = value
				answers = []	# Save all four answers in one list
				continue		# skip to next row
			
			# Find and save answers
			if ")" in value:
				# ~ split_answer_row = value.split()[1:]
				# ~ answer = ' '.join(split_answer_row)
				# ~ answers.append(answer.casefold())	# Ensure answer is all lower case
				answers.append(value[3:].casefold())
			if len(answers) == 4:
				Q.update({current_ID : answers})
			if "4)" in value:			
				continue				# skip to next row		
	
	return Q
			


########################################################################



# Collect all ID numbers and answers
answers = search_answers(df)


# Question IDs
qids = list(answers.keys())

# Make exceptions. Could import a list from separate docutment instead
exceps = ["a", "to", "the", "of", "in", "are", "is", "at", "by", "on", \
	"with", "as", "for", "from", "about", "because", "can't", "don't", \
	" can ", " do ", " will ", " all ", " up ",	"there", "this", "then",\
	"them", "they", "their", "those", "and"]

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



