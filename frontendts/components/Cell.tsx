import { Cell } from "../models/cells";
import Line from "./Line";
import { useState } from "react";
import { LineFactory } from "../services/line-factory";
import { faPlay } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface CellProps {
    id: number;
    cell: Cell;
    callApi: (_: string) => Promise<string>;
}

export default function CellComponent({id, cell, callApi}: CellProps) {
    const [result, setResult] = useState('');
    const [lines, setLines] = useState(cell.lines);

    const addLine = () => {
        const newLine = LineFactory.createCodeLine();
        setLines([...lines, newLine]);
    }

    const lineUpdate = (i: number, content: string) => {
        let l = lines;
        l[i].content = content;
        setLines(l);
    }
    
    const execLines = async () => {
        const results = [];
        for(let i=0; i<lines.length; i++){
            const r = await callApi(lines[i].content);
            results.push(r);
        }
        setResult(results.join('\n')); 
    }

    return (
        <div className="cell-component">
            <div className="cell-header">
                <h2>Cell #{id}</h2>
                <div onClick={execLines}>
                    <FontAwesomeIcon className="play-icon" icon={faPlay} />
                </div>
            </div>
            { lines.map((line, i) => <div className="sick-fade-in" key={i}><Line line={line} lineNumber={i} lineUpdate={lineUpdate}/></div>) }
            <div className="action-container">
                <div className="flex-grow"></div>
                <button className="icon-button" type="button" onClick={() => addLine()}>+</button>
            </div>
            <div>
                <h3>Result</h3>
                <pre>{result}</pre>
            </div>            
        </div>
    )
}