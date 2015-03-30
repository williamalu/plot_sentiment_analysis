"""
Parses through books in txt format and analyses sentiment for every chapter.

book_file_name is input string with the file name of the book's txt file
"""

import string
from pattern.en import *
#try to avoid import *s, just import functions as needed, or be explicit about which function from the module you are using when you call it.
import matplotlib.pyplot as plt

def plot_sentiment_analysis(book_file_name):
    #this is really nitpicking: this function got a bit long so it would have been nice to have another function to do some of the stuff here to make this function shorter and more readable.
	input_book = open(book_file_name,'r')

	#turns book's text file into list of strings
	input_book_lines = input_book.readlines()
	#strips newline characters from input_book_lines
	for line in range(len(input_book_lines)):
		input_book_lines[line] = input_book_lines[line].strip()
	#removes empty strings from input_book_lines
	input_book_lines = filter(None, input_book_lines)
#I like those readable function names!
	lines = strip_gutenberg_header(input_book_lines)
	lines = separate_chapters(lines)
	#calculates sentiment of each chapter
	all_sentiment = []
	for chap in lines:
		all_sentiment.append(sentiment(chap))
	#transforms sentiment from (polarity, subjectivity) to (polarity)(subjectivity)
	all_sentiment = zip(*all_sentiment)
	#calculates number of chapters in book
	num_chaps = [x+1 for x in range(len(lines))]
	#plots polarity vs. chapter #
	plt.plot(num_chaps,all_sentiment[0],'-o')
	plt.xlabel('Book Chapter #')
	plt.ylabel('Polarity')
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
		#finds what line a chapter begins and ends at
		if line.find('Chapter') == 0:
			chap_breaks.append((prev_break, line_num))
			prev_break = line_num + 1
		#finds last line of last chapter (must hard code in text)
		if line.find("can stop at Marcini's for a little dinner on the way") == 0:
			end_line = line_num + 1
			chap_breaks.append((prev_break, end_line))
	#removes empty first chapter break that only contains author information
	del chap_breaks[0]
        #never seen this before but its readable and stackoverflow seems to approve of it. glad I learned it from you!
	#turns data on where a chapter begins and ends and compiles list of strings, 
	#with each string containing the text for each chapter
	chap_texts = []
	for chap in range(len(chap_breaks)):
		start_line, end_line = chap_breaks[chap]
		chap_texts.append(reduce(lambda x,y: x + " " + y, lines[start_line:end_line]))
	return chap_texts


if __name__ == "__main__":
	plot_sentiment_analysis('hound_of_baskervilles.txt')
