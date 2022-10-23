import {AbstractLine} from "../models/cells";
import React, {useState, useEffect} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPlus, faTimes} from "@fortawesome/free-solid-svg-icons";
import Katex from "./Katex";

interface LineProps {
    lineNumber: Number;
    line: AbstractLine;
    lineUpdate: Function;
}

export default function Line({lineNumber, line, lineUpdate}: LineProps) {
    const [content, setContent] = useState(line.content);
    const [focus, setFocus] = useState(false);
    const textArea = React.createRef<HTMLTextAreaElement>();

    function handleChange(event: any): void {
        setContent(event.target.value);
    }

    function onFocus(): void {
        setFocus(true);
    }

    function onBlur(): void {
        setFocus(false);
    }

    function addSum(): void {
        setContent(`${content}\\sum_{i=0}^{n} i*i`);
        textArea.current?.select();
    }

    function addPlus(): void {
        setContent(`${content}+`);
        textArea.current?.select();
    }

    function addProduct(): void {
        setContent(`${content} \\prod_{i=1}^{n} i `);
        textArea.current?.select();
    }

    function addArrow(): void {
        setContent(`${content} \\leftarrow `);
        textArea.current?.select();
    }

    function addTimes(): void {
        setContent(`${content}\\times`);
        textArea.current?.select();
    }

    useEffect(()=>{
        lineUpdate(lineNumber, content);
    }, [lineNumber, lineUpdate, content]);

    return (
        <div>
            <div>
                <Katex instruction={content}/>
            </div>
            <div className={`line-container ${focus ? 'focused' : ''}`}>
                <div className="line-actions">
                    <button className="line-action" onClick={addSum}>Σ</button>
                    <button className="line-action font-bold" onClick={addArrow}>⟵</button>
                    <button className="line-action font-bold" onClick={addProduct}>𝝿</button>
                    {/* <button className="line-action" onClick={addPlus}><FontAwesomeIcon icon={faPlus} /></button>
                    <button className="line-action" onClick={addTimes}><FontAwesomeIcon icon={faTimes} /></button> */}

                </div>
                <textarea ref={textArea} className="line-area" onChange={handleChange} value={content} onFocus={onFocus} onBlur={onBlur}></textarea>
            </div>
        </div>
    )
}
