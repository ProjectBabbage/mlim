import {AbstractLine} from "../models/cells";
import React, {useState, useEffect} from "react";
import Katex from "./Katex";

interface LineProps {
    lineNumber: Number;
    line: AbstractLine;
    lineUpdate: Function;
    lineFocused: Function;
}

export default function Line({lineNumber, line, lineUpdate, lineFocused}: LineProps) {
    const [content, setContent] = useState(line.content);
    const [focus, setFocus] = useState(false);

    const textArea = React.createRef<HTMLTextAreaElement>();

    function handleChange(event: any): void {
        lineUpdate(lineNumber, event.target.value);
    }

    function onFocus(): void {
        setFocus(true);
        lineFocused(line, lineNumber)
    }

    function onBlur(): void {
        setFocus(false);
    }

    useEffect(() => {
        setContent(line.content)
    }, [line.content])

    return (
        <div>
            <div className="cursor-pointer">
                <Katex instruction={content}/>
            </div>
            <div className={`line-container ${focus ? 'focused' : ''}`}>
                <textarea ref={textArea} className="line-area" onChange={handleChange} value={content} onFocus={onFocus} onBlur={onBlur}></textarea>
            </div>
        </div>
    )
}
