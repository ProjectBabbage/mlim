import {AbstractLine} from "../models/cells";
import React, {useState} from "react";

interface LineProps {
    line: AbstractLine;
}

export default function Line(props: LineProps) {
    const [text, setText] = useState(props.line.content);

    function handleChange(event: any): void {
        setText(event.target.value);
    }

    return (
        <div>
            <textarea className="line-area" value={text} onChange={handleChange}></textarea>
        </div>
    )
}
