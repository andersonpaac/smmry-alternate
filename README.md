# SMMRY-Docs


# Objective
Takes a text file/article as input and outputs a summary of 
it. 

## Usage 
```
		python main.py -f sample-input-1.txt -o out.txt		
```
Will write summary to file using sample-input-1.txt as input
```
		python main.py -f sample-input-1.txt -o out.txt -opts ECHO_ON
```	
Will print to stdout
```
		python main.py -debug ON										
```
Will log to stdout


# Download the dependencies	
*smmry-alternate* requires the nltk libraries and can be downloaded as below
```	
sudo python -m nltk.downloader -d /usr/local/share/nltk_data all
```
