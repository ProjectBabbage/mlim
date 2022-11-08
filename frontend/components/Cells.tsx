import { faRefresh, faSave, faUpload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {useState, useRef, createContext, SyntheticEvent} from "react";
import {Cell} from "../models/cells";
import CellComponent from "./Cell";
import { getApi } from "../utils/requests"

export const CellsContext = createContext({}); 

export interface ICellsContext {
    cells: Array<Cell>;
    setCells: Function;
    deleteCell: Function;
    updateCell: Function;
}

const cellsContainerStyle = {
    border: "1px",
    width: "800px"
}

const Cells = () => {
    const fileInput = useRef()
    const [cells, setCells] = useState<Array<Cell>>([])
    const [title, setTitle] = useState('Document')

    const addCell = () => {
        const newCell: Cell = {
            id: cells.length ? cells[cells.length-1].id + 1: 1,
            content: ""
        }
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

    const updateCell = (cell: Cell) => {
        const cellsCopy = [...cells];
        let cId = cellsCopy.findIndex((c) => c.id === cell.id);
        cellsCopy[cId] = cell;
        setCells(cellsCopy);
    }

    const restartKernel = () => {
        getApi('/restart')
    }

    const saveFile = () => {
        const file = {title, cells}
        console.log("saving file")
        console.log(JSON.stringify(file))

        const link = document.createElement("a");
        link.download = `${title}.mlim`;
        link.href =
          "data:application/json;charset=utf-8," +
          encodeURIComponent(JSON.stringify(file));
        link.click();
    }

    const loadFile = (e: SyntheticEvent) => {
        if (e.target.files) {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.onload = () => {
                const file = JSON.parse(reader.result);
                setTitle(file.title)
                setCells(file.cells)
            };
            reader.readAsText(file);
        }
    }

    return (
        <div style={cellsContainerStyle}>
            <div className="flex items-center justify-between">
                <h1>{title}</h1>
                <div className="flex justify-end cursor-pointer space-x-4">
                    <FontAwesomeIcon icon={faRefresh} height={20} onClick={restartKernel} />
                    <FontAwesomeIcon icon={faSave} height={20} onClick={saveFile} />
                    <input hidden ref={fileInput} type="file" accept=".mlim" onChange={(e) => loadFile(e)} />   
                    <FontAwesomeIcon icon={faUpload} height={20} onClick={()=> fileInput?.current.click()} />
                </div>
            </div>
            <CellsContext.Provider value={{cells, setCells, updateCell, deleteCell}}>
                <div>
                    { cells.map((cell, i) => <CellComponent key={i}  cell={cell}/> ) }
                </div>
            </CellsContext.Provider>

            {/* NewCell */}
            <div className="action-container">
                <div className="flex-grow bg-white"></div>
                <div>
                    <button type="button" className="add-cell-action" onClick={addCell}>Nouvelle cellule</button>
                </div>
            </div>
        </div>
    )
}

export default Cells;
