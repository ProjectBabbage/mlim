#!/bin/sh

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
    echo "Usage: ./mlim.sh [ -h | --help ] [ -b | --back ] [ -f | --front ]
                 [ -r | --run ] [ -t | --tests ]
                 [ (-l | --lexer) TEST_FILE ] 
                 [ (-p | --parser) TEST_FILE ]"
}

args=( )
for arg; do
    case "${arg}" in
        --help)
            args+=( -h );;
        --back) 
            args+=( -b );;
        --front)
            args+=( -f );;
        --run)
            args+=( -r );;
        --tests) 
            args+=( -t );;
        --test-lexer) 
            args+=( -l );;
        --test-parser) 
            args+=( -p );;
        *) 
            args+=( "$arg" );;
    esac
done

eval set -- "${args[@]}"

while getopts hbfrtl:p: OPT; do
    case "${OPT}" in
        h)
            usage;;
        b) 
            back;;
        f) 
            front;;
        r)
            front &
            back;;
        t) 
            tests;;
        l) 
            python compiler/lexer.py ${OPTARG};;
        p) 
            python compiler/evaluation.py ${OPTARG};;
        *)
            echo "unrecognized option: ${OPT}"
            usage
            exit 2;;
    esac
done
