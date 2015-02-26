"""
Parses through books in txt format and analyses sentiment for every chapter.

book_file_name is input string with the file name of the book's txt file
"""

import string
from pattern.en import *
import matplotlib.pyplot as plt

def plot_sentiment_analysis(book_file_name):
	input_book = open(book_file_name,'r')

	#turns book's text file into list of strings
	input_book_lines = input_book.readlines()
	#strips newline characters from input_book_lines
	for line in range(len(input_book_lines)):
		input_book_lines[line] = input_book_lines[line].strip()
	#removes empty strings from input_book_lines
	input_book_lines = filter(None, input_book_lines)
	lines = strip_gutenberg_header(input_book_lines)
	lines = separate_chapters(lines)
	all_sentiment = []
	for chap in lines:
		all_sentiment.append(sentiment(chap))
	all_sentiment = zip(*all_sentiment)
	plt.plot((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),all_sentiment[1],'-o')
	plt.xlabel('Book Chapter #')
	plt.ylabel('Positivity')
	plt.title('Sentiment in each chapter of The Hound of the Baskervilles')
	plt.show()

def strip_gutenberg_header(input_book_lines):
	"""
	Strips Gutenberg Project header from book text files.
	"""
	lines = input_book_lines
	curr_line = 0
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
		curr_line += 1
	return lines[curr_line+1:]

def separate_chapters(lines):
	"""
	Separates chapters from each other for sentiment analysis
	"""
	prev_break = 0
	chap_breaks = []
	end_line = 0
	for line_num, line in enumerate(lines):
		if line.find('Chapter') == 0:
			chap_breaks.append((prev_break, line_num))
			prev_break = line_num + 1
		if line.find("can stop at Marcini's for a little dinner on the way") == 0:
			end_line = line_num + 1
			chap_breaks.append((prev_break, end_line))
	del chap_breaks[0]
	#print chap_breaks
	chap_texts = []
	for chap in range(len(chap_breaks)):
		start_line, end_line = chap_breaks[chap]
		chap_texts.append(reduce(lambda x,y: x + " " + y, lines[start_line:end_line]))
	#print len(chap_texts)
	#print "\n------------------------\n".join(chap_texts)
	return chap_texts


if __name__ == "__main__":
	plot_sentiment_analysis('hound_of_baskervilles.txt')