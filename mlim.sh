#!/bin/bash

export PYTHONPATH=.

front() {
    cd frontend
    npm run dev
}

back() {
    if ! [ -x "poetry -V" ]
    then poetry run uvicorn backend.app:app --reload --port 8080
    else uvicorn backend.app:app --reload --port 8080
    fi
}

tests() {
    python -m unittest discover
}

usage() {
    echo "Usage: ./mlim.sh [ -h | --help ] [ -t | --tests ] [ -i | --lint ]
                 [ -b | --back ] [ -f | --front ] [ -r | --run ]
                 [ (-l | --lexer) TEST_FILE ] 
                 [ (-p | --parser) TEST_FILE ]
                 [ (-e | --evaluation) TEST_FILE ]"
}

args=( )
for arg; do
    case "${arg}" in
        --help)
            args+=( -h );;
        --tests) 
            args+=( -t );;
        --lint)
            args+=( -i );;
        --back) 
            args+=( -b );;
        --front)
            args+=( -f );;
        --run)
            args+=( -r );;
        --lexer) 
            args+=( -l );;
        --parser) 
            args+=( -p );;
        --evaluation) 
            args+=( -e );;
        *) 
            args+=( "$arg" );;
    esac
done

eval set -- "${args[@]}"

while getopts htibfrl:p:e: OPT; do
    case "${OPT}" in
        h)
            usage;;
        t) 
            tests;;
        i)
            flake8;;
        b) 
            back;;
        f) 
            front;;
        r)
            front &
            back;;
        l) 
            python compiler/lexer.py ${OPTARG};;
        p) 
            python compiler/parser.py ${OPTARG};;
        e) 
            python compiler/evaluation.py ${OPTARG};;
        *)
            echo "Unrecognized option \"$1\""
            usage
            exit 2;;
    esac
done
