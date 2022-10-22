import { AbstractLine, Cell } from "../models/cells";
import Line from "./Line";
import { useState } from "react";
import { LineFactory } from "../services/line-factory";
import { faPlay, faTrashCan, faPlus, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface CellProps {
    id: number;
    cell: Cell;
    deleteCell: Function;
    callApi: (_: string) => Promise<string>;
}

export default function CellComponent({id, cell, deleteCell, callApi}: CellProps) {
    const [result, setResult] = useState('');
    const [lines, setLines] = useState(cell.lines);
    const [editorEnabled, setEditorEnabled] = useState(true);
    const [currentLineIndex, setCurrentLineIndex] = useState<number | null>(null);

    function toggleEditor(): void {
        setEditorEnabled(!editorEnabled)
    }

    const addLine = () => {
        const newLine = LineFactory.createCodeLine();
        setLines([...lines, newLine]);
        setCurrentLineIndex(currentLineIndex ? currentLineIndex + 1 : 0)
    }

    const lineUpdate = (lineIndex: number, content: string) => {
        /*
            We have to create a new instance of the list 
            to ensure triggering functions useEffect 
        */
        let l = []; 
        for(let i = 0 ; i<lines.length ; i++){
            if(i === lineIndex){
                let newLine = null
                switch(lines[i].type){
                    case 'code':
                        newLine = LineFactory.createCodeLine()
                        break;
                    case 'text':
                        newLine = LineFactory.createTextLine()
                        break;
                }
                newLine.content = content
                l.push(newLine)
            }
            else{
                l.push(lines[i])
            }
        }
        setLines(l);
    }

    const lineFocused = (line: AbstractLine, index: number) => {
        setCurrentLineIndex(index)
    }
    
    const nextLine = () => {
        if(currentLineIndex == lines.length - 1)
            addLine()
        else
            setCurrentLineIndex(currentLineIndex === null ? 0 : currentLineIndex + 1);
    }

    const previousLine = () => {
        if(currentLineIndex && currentLineIndex > 0){
            setCurrentLineIndex(currentLineIndex - 1)
        }
    }

    const execLines = async () => {
        const results = [];
        for(let i=0; i<lines.length; i++){
            const r = await callApi(lines[i].content);
            results.push(r);
        }
        setResult(results.join('\n')); 
    }

    function addSum(): void {
        if(currentLineIndex !== null)
            lineUpdate(currentLineIndex, `${lines[currentLineIndex].content}\\sum_{i=0}^{n} i*i`)

    }

    function addPlus(): void {
        if(currentLineIndex !== null)
            lineUpdate(currentLineIndex, `${lines[currentLineIndex].content}+`)
    }

    function addTimes(): void {
        if(currentLineIndex !== null)
            lineUpdate(currentLineIndex, `${lines[currentLineIndex].content}\\times`)
    }

    return (
        <div className="cell-component">
            <div className="cell-header">
                <div className="text-red-500" onClick={() => deleteCell(id)}>
                    <FontAwesomeIcon icon={faTrashCan} />
                </div>            
                <h2>Cell #{id}</h2>
                <div onClick={execLines}>
                    <FontAwesomeIcon className="play-icon" icon={faPlay} />
                </div>
            </div>
            <div className="line-actions">
                <button className="line-action" onClick={addSum}>Σ</button>
                <button className="line-action" onClick={addPlus}><FontAwesomeIcon icon={faPlus} /></button>
                <button className="line-action" onClick={addTimes}><FontAwesomeIcon icon={faTimes} /></button>
                <div className="flex-grow cursor-pointer" onClick={() => toggleEditor()}></div>
            </div>
            <div className="lines-container">
                { lines.map((line, i) => 
                    <div className="sick-fade-in" key={`${id}${i}`}>
                        <Line
                            line={line} 
                            lineNumber={i} 
                            lineUpdate={lineUpdate} 
                            lineFocused={lineFocused} 
                            nextLine={nextLine}
                            previousLine={previousLine}
                            shouldFocus={i === currentLineIndex}/>
                    </div>) }
            </div>
            <div className="action-container">
                <div className="flex-grow"></div>
                <button className="icon-button" type="button" onClick={() => addLine()}>+</button>
            </div>
            <div>
                <pre>{result}</pre>
            </div>
        </div>
    )
}