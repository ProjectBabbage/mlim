import { useState, useContext } from "react";
import { Cell } from "../models/cells";
import { CellsContext, ICellsContext } from "./Cells";
import CellContent from "./CellContent";
import CellHeader from "./CellHeader";
import { postApi } from "../utils/requests"
import Katex from "./Katex";


interface CellProps {
    cell: Cell;
}

const CellComponent = ({cell}: CellProps) => {
    const {updateCell} = useContext(CellsContext) as ICellsContext
    const [editorEnabled, setEditorEnabled] = useState(true)
    const [result, setResult] = useState('');

    const executeCell = async () => {
        const {response, msg} = await postApi('/code/', cell.content);
        setResult([response, msg].join(' ')); 
    }
    const addOperator = (operator: string) => {
        updateContent(`${cell.content} ${operator}`)
    }

    const updateContent = (content: string) => {
        updateCell({...cell, content})
    }

    return (
        <div className="cell-component">
            <CellHeader cellId={cell.id} executeAction={executeCell} addOperator={addOperator} setEditorEnabled={setEditorEnabled} />
            <CellContent content={cell.content} updateContent={updateContent} executeAction={executeCell} editorEnabled={editorEnabled} setEditorEnabled={setEditorEnabled} />

            {/* Result */}
            { result.trim() && 
            <div className="cell-result">
                <hr />
                <Katex instruction={result}></Katex>
            </div>
            }
        </div>
    )
}

export default CellComponent;
