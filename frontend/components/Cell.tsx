import { useState } from "react";
import { Cell } from "../models/cells";
import CellContent from "./CellContent";
import CellHeader from "./CellHeader";
import { callApi } from "../utils/requests"


interface CellProps {
    cell: Cell;
    deleteCell: Function;
}

const CellComponent = ({cell, deleteCell}: CellProps) => {
    const [content, setContent] = useState('');
    const [result, setResult] = useState('');

    const executeCell = async () => {
        const {response, msg} = await callApi(content);
        setResult([response, msg].join(' ')); 
    }

    const addOperator = (operator: string) => {
        setContent(`${content} ${operator}`)
    }

    return (
        <div className="cell-component">
            <CellHeader cellId={cell.id} deleteAction={deleteCell} executeAction={executeCell} addOperator={addOperator}/>
            <CellContent content={content} setContent={setContent} executeAction={executeCell} />
            <div className="cell-result">
                <pre>{result}</pre>
            </div>
        </div>
    )
}

export default CellComponent;
