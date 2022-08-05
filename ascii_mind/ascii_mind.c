/*Copyright 2020 Thomas van Maaren

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*/



//mastermind [slots] [letters]
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

#define black 2
#define white 1
#define blank 0



void flush_input(){
	int ch;
	while((ch =getchar()) != '\n' && ch != EOF);
}

void feedback(int slots, int*blacks,int*whites,char*input, char*Solution){
	*blacks=0;
	*whites=0;
	int Feedback[slots];
	int i = 0;
	while(i<slots){
		Feedback[i]=blank;
		if(input[i]==Solution[i]){
			Feedback[i] = black;
			(*blacks)++;
		}
		i++;
	}
	//check for whites
	i = 0;
	//go through all non-black Answers
	while(i<slots){
		if(Feedback[i] != black){
			char Comp = input[i];
			int ii=0;
			//find a solution that is the same as the answer, that isn't already marked as black or white
			while(ii<slots){
				if(blank==Feedback[ii] && Comp==Solution[ii]){
				       Feedback[ii] = white;
				       (*whites)++;
				       break;
				}	
				ii++;
			}
		}
		i++;
	}
}

long int possibillities(int slots,int letters, char**input, int*blacks, int*whites, int guess){
	long int answer=0;
	char try[slots];
	int i=0;
	while(i<slots){
		try[i]='!';
		i++;
	}
	//loop that goes through all posible answers a user can fill in
	while(1){
		int tryblacks;
		int trywhites;
		//loops through all the guesses
		int i=0;
		while(1){
			feedback(slots, &tryblacks,&trywhites,input[i], try);
			if(!(trywhites == whites[i] && tryblacks == blacks[i])){
				break;
			}
			i++;
			if(i>guess){
				//printf("%s\n",try);
				answer++;
				break;
			}
		}
		i=0;//keeps track of which character it should increment
NextChar:	if(i>=slots){
			break;
		}
		try[i]++;
		if(try[i]>'!'+letters-1){
			try[i]='!';
			i++;
			goto NextChar;
		}
	}

	return answer;
}

int main(int argc, char**argv){
	//check if the right amount of arguments is given
	if(argc!=3){
		printf("error: Not the right amount of arguments given\n"
		    	"You should right in this form: %s [slots] [ascii-characters]\n",argv[0]);
		return 1;
	}
	int 	slots 		= 	atoi(argv[1]);
	if(slots<1){
		printf("There has to be a minimum of one slot");
		exit(1);
	}
	int 	letters 	=	atoi(argv[2]);
	if(letters<1){
		printf("There has to be a minimum of one character");
		exit(2);
	}
	if(letters>94){
		printf("There are only 94 possible character");
		exit(3);
	}

	srand(time(NULL));

	//tell the user which characters per can use
	printf("The possible characters are:");
	int i =0;
	while(i<letters){
		printf("%c", 33+i);
		i++;
	}
	printf("\n");

	//make random letter sequence
	char*Solution;
	Solution = malloc(sizeof(char)*slots);
	i=0;
	while(i<slots){
		Solution[i] = (rand()%(letters)+33);
		i++;	
	}
	char**answer=malloc(sizeof(char*));
	int*amblack=malloc(sizeof(int));
	int*amwhite=malloc(sizeof(int));
	//gameloop
	i=0;
	while(1){
		//retrieve guess from user
		printf("Guess %d:",i+1);
		char *Answer=malloc(sizeof(char)*slots);
		scanf("%s", Answer);
		flush_input();

		//give feedback on how good the guess was
		
		//Check for blacks
		feedback(slots,&(amblack[i]), &(amwhite[i]), Answer, Solution);

		answer[i]=Answer;
		printf("Black:%d\n", amblack[i]);
		printf("White:%d\n", amwhite[i]);
		printf("possibillities:%ld\n",possibillities(slots,letters,  answer, amblack, amwhite, i));
		i++;
		amblack=realloc(amblack, (i+1)*sizeof(int));
		amwhite=realloc(amwhite, (i+1)*sizeof(int));
		answer =realloc(answer, (i+1)*sizeof(char*));
	}
}
