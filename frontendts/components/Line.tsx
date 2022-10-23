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

<<<<<<< HEAD
    useEffect(() => {
        if(textArea.current){
            textArea.current.selectionStart = cursorPosition
            textArea.current.selectionEnd = cursorPosition
        }
    }, [textArea, cursorPosition])
||||||| parent of 202f4d6 (feat: calls)
    function addTimes(): void {
        setContent(`${content}\\times`);
        textArea.current?.select();
    }

    useEffect(()=>{
        lineUpdate(lineNumber, content);
    }, [lineNumber, lineUpdate, content]);
=======
   function addMapsto(): void {
        setContent(`${content} \\mapsto `);
        textArea.current?.select();
    }

    function addTimes(): void {
        setContent(`${content}\\times`);
        textArea.current?.select();
    }

    useEffect(()=>{
        lineUpdate(lineNumber, content);
    }, [lineNumber, lineUpdate, content]);
>>>>>>> 202f4d6 (feat: calls)

    return (
        <div>
            <div className="cursor-pointer" onClick={() => toggleEditor()}>
                <Katex instruction={content}/>
            </div>
            { (editorEnabled || content.length === 0) &&
            <div className={`line-container ${focus ? 'focused' : ''}`}>
<<<<<<< HEAD
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
||||||| parent of 202f4d6 (feat: calls)
                <div className="line-actions">
                    <button className="line-action" onClick={addSum}>Σ</button>
                    <button className="line-action font-bold" onClick={addProduct}>𝝿</button>
                    {/* <button className="line-action" onClick={addPlus}><FontAwesomeIcon icon={faPlus} /></button>
                    <button className="line-action" onClick={addTimes}><FontAwesomeIcon icon={faTimes} /></button> */}

                </div>
                <textarea ref={textArea} className="line-area" onChange={handleChange} value={content} onFocus={onFocus} onBlur={onBlur}></textarea>
=======
                <div className="line-actions">
                    <button className="line-action" onClick={addSum}>Σ</button>
                    <button className="line-action font-bold" onClick={addProduct}>𝝿</button>
                    <button className="line-action font-bold" onClick={addMapsto}>↦</button>
                    {/* <button className="line-action" onClick={addPlus}><FontAwesomeIcon icon={faPlus} /></button>
                    <button className="line-action" onClick={addTimes}><FontAwesomeIcon icon={faTimes} /></button> */}

                </div>
                <textarea ref={textArea} className="line-area" onChange={handleChange} value={content} onFocus={onFocus} onBlur={onBlur}></textarea>
>>>>>>> 202f4d6 (feat: calls)
            </div>
            }
        </div>
    )
}
