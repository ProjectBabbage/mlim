import { AbstractLine, Cell } from "../models/cells";
import Line from "./Line";
import { useState } from "react";
import { LineFactory } from "../services/line-factory";
import { faPlay, faTrashCan, faPlus, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface CellProps {
    cell: Cell;
    deleteCell: Function;
    callApi: (_: string) => Promise<string>;
}

export default function CellComponent({cell, deleteCell, callApi}: CellProps) {
    const [result, setResult] = useState('');
    const [lines, setLines] = useState(cell.lines);
    const [editorEnabled, setEditorEnabled] = useState(true);
    const [currentLineIndex, setCurrentLineIndex] = useState<number>(0);
    const [currentCursorCol, setCurrentCursorCol] = useState<number>(0);

    function toggleEditor(): void {
        setEditorEnabled(!editorEnabled)
    }

    const addLine = () => {
        const newLine = LineFactory.createCodeLine();
        setLines([...lines, newLine]);
        setCurrentLineIndex(currentLineIndex + 1)
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

    const lineFocused = (index: number) => {
        setCurrentLineIndex(index)
    }
    
    const nextLine = () => {
        if(currentLineIndex == lines.length - 1)
            addLine()
        else
            setCurrentLineIndex(currentLineIndex === null ? 0 : currentLineIndex + 1);
    }

    const lineDelete = (i: number) => {
        if(currentLineIndex===0) return;
        lines.splice(i, 1);
        setLines([...lines]);
        previousLine();
    }

    const previousLine = () => {
        if(currentLineIndex && currentLineIndex > 0){
            setCurrentLineIndex(currentLineIndex - 1)
        }
    }

    const cursorPositionMoved = (lineNumber: number, cursorPosition: number) => {
        if(lineNumber==currentLineIndex){
            setCurrentCursorCol(cursorPosition)
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

    function appendAtCursor(value: string): void {
        let before = lines[currentLineIndex].content.substring(0,currentCursorCol-1)
        let after = lines[currentLineIndex].content.substring(currentCursorCol-1)
        
        lineUpdate(currentLineIndex,`${before}${value}${after}`);
        setCurrentCursorCol(currentCursorCol+value.length)
    }

    function addSum(): void {
        if(currentLineIndex !== null)
            appendAtCursor(` \\sum_{i=0}^{n} i*i `)

    }

    function addProduct(): void {
        if(currentLineIndex !== null)
            appendAtCursor(` \\prod_{i=1}^{n} i `)
    }

    function addArrow(): void {
        if(currentLineIndex !== null)
            appendAtCursor(` \\leftarrow `)
    }

    return (
        <div className="cell-component">
            <div className="cell-header">
                <div className="text-red-500 cursor-pointer" onClick={() => deleteCell(cell.id)}>
                    <FontAwesomeIcon icon={faTrashCan} />
                </div>            
                <h2>Cell #{cell.id}</h2>
                <div className="cursor-pointer" onClick={execLines}>
                    <FontAwesomeIcon className="play-icon" icon={faPlay} />
                </div>
            </div>
            <div className="line-actions">
                <button className="line-action font-bold" onClick={addArrow}>⟵</button>
                <button className="line-action" onClick={addSum}>Σ</button>
                <button className="line-action font-bold" onClick={addProduct}>𝝿</button>
                <div className="flex-grow cursor-pointer" onClick={() => toggleEditor()}></div>
            </div>
            <div className="lines-container">
                { editorEnabled && lines.map((line, i) => 
                    <div className="sick-fade-in" key={`${cell.id}${i}`}>
                        <Line
                            line={line} 
                            lineNumber={i} 
                            lineUpdate={lineUpdate}
                            lineDelete={lineDelete}
                            lineFocused={lineFocused} 
                            nextLine={nextLine}
                            previousLine={previousLine}
                            shouldFocus={i === currentLineIndex}
                            cursorPositionUpdate={cursorPositionMoved}
                            cursorPosition={currentCursorCol}/>
                    </div>) }
            </div>
            <div>
                <pre>{result}</pre>
            </div>
        </div>
    )
}