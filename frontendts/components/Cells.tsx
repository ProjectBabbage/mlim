import {useState} from "react";
import {Cell} from "../models/cells";
import CellComponent from "./Cell";
import {CellFactory} from "../services/cell-factory";
import {LineFactory} from "../services/line-factory";
import Chart from "./Chart";


export default function Cells() {
    const [cells, setCells] = useState<Array<Cell>>([])
    
    async function callApi(command: string) {
        let response = await fetch("http://localhost:8080/code/", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify({
            code: command,
            }),
        });
        let result = await response.json().then((data) => data.RESULT);
        return result;
    }

    const addCell = () => {
        const newCell: Cell = CellFactory.createCell();
        newCell.lines.push(LineFactory.createCodeLine());
        setCells([...cells, newCell]);
    }
    
    const deleteCell = (i: number) => {
        cells.splice(i, 1);
        setCells([...cells]);
    }

    return (
        <div className="container">
            <h1>MLIM</h1>
            { cells.map((cell, i) => <div id={`cell${i}`} key={i}><CellComponent cell={cell} deleteCell={deleteCell} callApi={callApi} id={i}></CellComponent></div>) }
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