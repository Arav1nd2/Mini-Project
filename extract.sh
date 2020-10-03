#!/bin/bash


mkdir output
mkdir output/D
mkdir output/ND

cnt=0
for audio in ./Audio/D/*
do
    commandToExec="./SMILExtract -C ./config/IS09_emotion.conf -I ${audio} -csvoutput ./output/D/${cnt}.csv"
    echo "Executing: ${commandToExec} ....."
    eval $commandToExec
    echo "Stored Output in ./output/D/${cnt}.csv"
    ((cnt=cnt+1))
done
((cnt=0))
for audio in ./Audio/ND/*
do
    commandToExec="./SMILExtract -C ./config/IS09_emotion.conf -I ${audio} -csvoutput ./output/ND/${cnt}.csv"
    echo "Executing: ${commandToExec} ....."
    eval $commandToExec
    echo "Stored Output in ./output/ND/${cnt}.csv"
    ((cnt=cnt+1))
done
