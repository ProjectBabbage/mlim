import { faPowerOff } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {useState} from "react";
import {Cell} from "../models/cells";
import {CellFactory} from "../services/cell-factory";
import CellComponent from "./Cell";
import { getApi } from "../utils/requests"

const cellsContainerStyle = {
    border: "1px",
    width: "800px"
}

const Cells = () => {

    const [cells, setCells] = useState<Array<Cell>>([])

    const addCell = () => {
        const newCell: Cell = CellFactory.createCell();
        setCells([...cells, newCell]);
    }
    
    const deleteCell = (cellId: number) => {
        const cellsCopy = [...cells];

        const cellIdx = cellsCopy.findIndex((cell) => cell.id === cellId);
        if (cellIdx >= 0) {
            cellsCopy.splice(cellIdx, 1);
            setCells([...cellsCopy]);
        }
    }

    const restartKernel = () => {
        getApi('/restart')
    }

    return (
        <div style={cellsContainerStyle}>
            <h1>MLIM</h1>
            <div className="flex justify-end">
                <FontAwesomeIcon icon={faPowerOff} height={20} onClick={restartKernel} />
            </div>
            <div>
            { cells.map((cell, i) => <CellComponent key={i}  cell={cell} deleteCell={deleteCell}/> ) }
            </div>

            {/* NewCell */}
            <div className="action-container">
                <div className="flex-grow"></div>
                <div>
                    <button type="button" className="add-cell-action" onClick={addCell}>Nouvelle cellule</button>
                </div>
            </div>
        </div>
    )
}

export default Cells;
