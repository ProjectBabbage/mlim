import {AbstractLine} from "../models/cells";
import React, {useState, useEffect} from "react";
import Katex from "./Katex";

interface LineProps {
    lineNumber: Number;
    cursorPosition: number;
    line: AbstractLine;
    lineUpdate: Function;
    lineDelete: Function;
    lineFocused: Function;
    nextLine: Function;
    previousLine: Function;
    cursorPositionUpdate: Function
    shouldFocus: boolean
}

export default function Line({lineNumber, line, lineUpdate, lineDelete, lineFocused, nextLine, previousLine, shouldFocus, cursorPositionUpdate, cursorPosition}: LineProps) {
    const [content, setContent] = useState(line.content);
    const [focus, setFocus] = useState(shouldFocus);
    const [editorEnabled, setEditorEnabled] = useState(true);

    const textArea = React.createRef<HTMLInputElement>();

    function handleChange(event: any): void {
        lineUpdate(lineNumber, event.target.value);
        if(textArea.current)
            cursorPositionUpdate(lineNumber, textArea.current.selectionStart)
    }

    function handleKeyDown(event: any): void {
        let key = event.key
        switch(key){
            case "Enter":
                nextLine();
                break;
            case "Backspace":
                if(content==''){
                    lineDelete();
                }
                break;
        }
        if(textArea.current)
            cursorPositionUpdate(lineNumber, textArea.current.selectionStart)
    }

    function onClick(): void {
        console.log(lineNumber)
        setFocus(true);
        lineFocused(lineNumber)
    }

    function onBlur(): void {
        setFocus(false);
    }

    function toggleEditor(): void{
        setEditorEnabled(!editorEnabled)
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

    useEffect(() => {
        if(textArea.current){
            textArea.current.selectionStart = cursorPosition
            textArea.current.selectionEnd = cursorPosition
        }
    }, [textArea, cursorPosition])

    return (
        <div>
            <div className="cursor-pointer" onClick={() => toggleEditor()}>
                <Katex instruction={content}/>
            </div>
            { (editorEnabled || content.length === 0) &&
            <div className={`line-container ${focus ? 'focused' : ''}`}>
                <input 
                    type="text" 
                    ref={textArea} 
                    className="line-area" 
                    onChange={handleChange} 
                    onKeyDown={handleKeyDown}
                    value={content}
                    onClick={onClick}
                    onBlur={onBlur}
                    placeholder="fill me up !"
                />
            </div>
            }
        </div>
    )
}
