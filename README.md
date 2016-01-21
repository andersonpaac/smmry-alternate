#SMMRY-Docs


#Objective
Takes a text file or a massive string as input and outputs a summary of 
it. 

##Usage 
		python main.py -f sample-input-1.txt -o out.txt					#Will write summary to file using sample-input-1.txt as input
		python main.py -f sample-input-1.txt -o out.txt -opts ECHO_ON	#Will print to stdout
		python main.py -debug ON										#Logs to stdout
	
	
	
#To Do
1.	Setup classes Text, Para, Sentence
2.	Setup Logging
3.	Setup Scoring
4.	Setup click
5.	Unit-tests	
6.	setup.py


##Classes

###Text
Holds the actual text of the entire document and holds an array of paras object.

	
