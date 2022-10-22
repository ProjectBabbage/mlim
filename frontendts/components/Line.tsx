import {AbstractLine} from "../models/cells";
import React, {useState, useEffect} from "react";
import Katex from "./Katex";

interface LineProps {
    lineNumber: Number;
    line: AbstractLine;
    lineUpdate: Function;
    lineFocused: Function;
    nextLine: Function;
    previousLine: Function;
    shouldFocus: boolean
}

export default function Line({lineNumber, line, lineUpdate, lineFocused, nextLine, previousLine, shouldFocus}: LineProps) {
    const [content, setContent] = useState(line.content);
    const [focus, setFocus] = useState(shouldFocus);

    const textArea = React.createRef<HTMLInputElement>();

    function handleChange(event: any): void {
        lineUpdate(lineNumber, event.target.value);
    }

    function handleKeyDown(event: any): void {
        let key = event.key
        switch(key){
            case "ArrowDown":
                nextLine();
                break;
            case "ArrowUp":
                previousLine();
                break;
        }
    }

    function onFocus(): void {
        setFocus(true);
        lineFocused(line, lineNumber)
    }

    function onBlur(): void {
        setFocus(false);
    }

    useEffect(() => {
        if(textArea.current && shouldFocus)
            textArea.current.focus()
        else
            onBlur()
    }, [textArea, shouldFocus])

    useEffect(() => {
        setContent(line.content)
    }, [line.content])

    return (
        <div>
            <div className="cursor-pointer">
                <Katex instruction={content}/>
            </div>
            <div className={`line-container ${focus ? 'focused' : ''}`}>
                <input 
                    type="text" 
                    ref={textArea} 
                    className="line-area" 
                    onChange={handleChange} 
                    onKeyDown={handleKeyDown}
                    value={content} 
                    onFocus={onFocus} 
                    onBlur={onBlur}
                />
            </div>
        </div>
    )
}
