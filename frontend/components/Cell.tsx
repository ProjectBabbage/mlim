import { useState } from "react";
import { Cell } from "../models/cells";
import CellContent from "./CellContent";
import CellHeader from "./CellHeader";
import { postApi } from "../utils/requests"
import Katex from "./Katex";


interface CellProps {
    cell: Cell;
    deleteCell: Function;
}

const CellComponent = ({cell, deleteCell}: CellProps) => {
    const [editorEnabled, setEditorEnabled] = useState(true)
    const [content, setContent] = useState('');
    const [result, setResult] = useState('');

    const executeCell = async () => {
        const {response, msg} = await postApi('/code/', content);
        setResult([response, msg].join(' ')); 
    }

    const addOperator = (operator: string) => {
        setContent(`${content} ${operator}`)
    }

    return (
        <div className="cell-component">
            <CellHeader cellId={cell.id} deleteAction={deleteCell} executeAction={executeCell} addOperator={addOperator} setEditorEnabled={setEditorEnabled} />
            <CellContent content={content} setContent={setContent} executeAction={executeCell} editorEnabled={editorEnabled} setEditorEnabled={setEditorEnabled} />

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
