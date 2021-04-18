#include<iostream>
#include<fstream>
#include<map>
#include<string>
#include<stdio.h>
#include<math.h>
#include"gem5/m5ops.h"
using namespace std;

#define REF_START 0
#define REF_NUM 250

#define USER_START 251
#define USER_NUM 1

#define DATASET_DIR string("myWorkDir/app/docDist/dataset/")
 
typedef std::map<std::string,int> strintmap;
 
 
void countwords(std::istream &in, strintmap &words){
    std::string s;
    while (in >> s){
        ++words[s];
    }
}
 
int computedistance(strintmap& d1, strintmap& d2){
    int dotproduct = 0;
    for (strintmap::iterator p1 = d1.begin(); p1 != d1.end(); p1++){
        strintmap::iterator p2 = d2.find(p1->first);
        if (p2 != d2.end())
            dotproduct += (p1->second*p2->second);
    }
    return dotproduct;
}
 
int main(int argc, char* argv[]){

    // STEP1: read the files
    ifstream refFile[REF_NUM], userFile[USER_NUM];
    for (int i = 0; i < REF_NUM; i++) {
        refFile[i].open(DATASET_DIR + to_string(REF_START+i) + string(".txt"), ios::in);
    }
    for (int i = 0; i < USER_NUM; i++) {
        userFile[i].open(DATASET_DIR + to_string(USER_START+i) + string(".txt"), ios::in);
    }


    // STEP2: change file into map
    strintmap refDoc[REF_NUM], userDoc[USER_NUM];
    for (int i = 0; i < REF_NUM; i++) {
        countwords(refFile[i], refDoc[i]);
    }
    for (int i = 0; i < USER_NUM; i++) {
        countwords(userFile[i], userDoc[i]);
    }


    // STEP3: ROI
    printf("[before checkpoint] Hello world!\n");
    m5_checkpoint(0, 0);
    printf("[after checkpoint] Hello world!\n");


    // STEP4: compare file
    int dotproduct[USER_NUM][REF_NUM];
    for (int i = 0; i < USER_NUM; i++) {
        for (int j = 0; j < REF_NUM; j++) {
            dotproduct[i][j] = computedistance(userDoc[i], refDoc[j]);
        }
    }


    cout << "--finish--" << "\n";
    return 0;
}
