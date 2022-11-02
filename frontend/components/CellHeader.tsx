import { faPlay, faTrashCan } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useContext } from "react"
import { CellsContext, ICellsContext } from "./Cells"

interface CellHeaderProps {
    cellId: number;
    executeAction: Function;
    addOperator: Function;
    setEditorEnabled: Function;
}

const CellHeader = ({cellId, executeAction, addOperator, setEditorEnabled}: CellHeaderProps) => {
    const { deleteCell } = useContext(CellsContext) as ICellsContext;
    const addSum = () =>{
        addOperator(` \\sum_{i=0}^{n} i*i `)
    }
    
    const addProduct = () => {
        addOperator(` \\prod_{i=1}^{n} i `)
    }
    
    const addMapsto = () => {
        addOperator(` \\mapsto `)
    }
    
    const addNabla = () => {
        addOperator(` \\nabla `)
    }

    const addMatrix = () => {
        addOperator(`\\begin{bmatrix} 1 & 2 & 3 \\\\ 4 & 5 & 6 \\end{bmatrix}`)
    }

    return (
        <div className="cell-header">
            <div className="flex justify-between items-center">
                <div className="text-red-500 cursor-pointer" onClick={() => deleteCell(cellId)}>
                    <FontAwesomeIcon icon={faTrashCan} width={15} />
                </div>            
                <h2>Cell #{cellId}</h2>
                <div className="cursor-pointer text-green-400" onClick={() => executeAction()}>
                    <FontAwesomeIcon icon={faPlay} width={15} />
                </div>
            </div>
            <div className="operator-actions" onClick={() => setEditorEnabled(true)}>
                <button className="operator-action font-bold" onClick={addMatrix}>[]</button>
                <button className="operator-action" onClick={addSum}>∑</button>
                <button className="operator-action font-bold" onClick={addProduct}>∏</button>
                <button className="operator-action font-bold" onClick={addMapsto}>↦</button>
                <button className="operator-action font-bold" onClick={addNabla}>∇</button>
            </div>
        </div>
    )
}

export default CellHeader;
