import {AbstractLine} from "../models/cells";
import React, {useState} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPlus, faTimes} from "@fortawesome/free-solid-svg-icons";

interface LineProps {
    line: AbstractLine;
}

export default function Line(props: LineProps) {
    const [text, setText] = useState(props.line.content);
    const [focus, setFocus] = useState(false);
    const textArea = React.createRef<HTMLTextAreaElement>();

    function handleChange(event: any): void {
        setText(event.target.value);
        console.log('Content changed')
    }

    function onFocus(): void {
        setFocus(true);
    }

    function onBlur(): void {
        setFocus(false);
    }

    function addSum(): void {
        setText(`${text}\\sum`);
        textArea.current?.select();
    }

    function addPlus(): void {
        setText(`${text}+`);
        textArea.current?.select();
    }

    function addTimes(): void {
        setText(`${text}\\times`);
        textArea.current?.select();
    }

    return (
        <div className={`line-container ${focus ? 'focused' : ''}`}>
            <div className="line-actions">
                <button className="line-action" onClick={addSum}>Σ</button>
                <button className="line-action" onClick={addPlus}><FontAwesomeIcon icon={faPlus} /></button>
                <button className="line-action" onClick={addTimes}><FontAwesomeIcon icon={faTimes} /></button>
            </div>
            <textarea ref={textArea} className="line-area" onChange={handleChange} value={text} onFocus={onFocus} onBlur={onBlur}></textarea>
        </div>
    )
}
