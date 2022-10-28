import { faPlay, faTrashCan } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface CellHeaderProps {
    cellId: number;
    deleteAction: Function;
    executeAction: Function;
    addOperator: Function;
}

const CellHeader = ({cellId, deleteAction, executeAction, addOperator}: CellHeaderProps) => {
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

    return (
        <div className="cell-header">
            <div className="cell-actions">
                <div className="text-red-500 cursor-pointer" onClick={() => deleteAction(cellId)}>
                    <FontAwesomeIcon icon={faTrashCan} />
                </div>            
                <h2>Cell #{cellId}</h2>
                <div className="cursor-pointer" onClick={() => executeAction()}>
                    <FontAwesomeIcon className="play-icon" icon={faPlay} />
                </div>
            </div>
            <div className="operator-actions">
                <button className="operator-action" onClick={addSum}>∑</button>
                <button className="operator-action font-bold" onClick={addProduct}>∏</button>
                <button className="operator-action font-bold" onClick={addMapsto}>↦</button>
                <button className="operator-action font-bold" onClick={addNabla}>∇</button>
            </div>
        </div>
    )
}

export default CellHeader;
