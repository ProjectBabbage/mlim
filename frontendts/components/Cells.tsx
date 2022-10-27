import {useState} from "react";
import {Cell} from "../models/cells";
import CellComponent from "./Cell";
import {CellFactory} from "../services/cell-factory";
import {LineFactory} from "../services/line-factory";
import Chart from "./Chart";

export default function Cells() {
    const [cells, setCells] = useState<Array<Cell>>([])
    

    async function callApi(command: string) {
        let result = await fetch("http://localhost:8080/code/", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify({
            code: command,
            }),
        });
        const {response, msg} = await result.json().then((data) => data);
        return {response, msg}
    }

    const addCell = () => {
        const newCell: Cell = CellFactory.createCell();
        newCell.lines.push(LineFactory.createCodeLine());
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

    return (
        <div className="container">
            <h1>MLIM</h1>
            { cells.map((cell, i) => <div id={`cell${i}`} key={cell.id}><CellComponent cell={cell} deleteCell={deleteCell} callApi={callApi}></CellComponent></div>) }
            <div className="action-container">
                <div className="flex-grow"></div>
                <div>
                    <button type="button" className="add-cell-action" onClick={addCell}>Nouvelle cellule</button>
                </div>
            </div>

            <Chart />
        </div>
    )
}
