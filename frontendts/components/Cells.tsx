import {useState} from "react";
import {Cell} from "../models/cells";
import CellComponent from "./Cell";
import {CellFactory} from "../services/cell-factory";
import {LineFactory} from "../services/line-factory";

export default function Cells() {
    const [cells, setCells] = useState<Array<Cell>>([])

    function addCell(): void {
        const newCell: Cell = CellFactory.createCell();
        newCell.lines.push(LineFactory.createCodeLine());
        setCells([...cells, newCell]);
    }

    return (
        <div className="container">
            <h1>My Cells</h1>
            { cells.map((cell, i) => <div id={`cell${i}`} key={i}><CellComponent cell={cell}></CellComponent></div>) }
            <div className="action-container">
                <div className="flex-grow"></div>
                <div>
                    <button type="button" onClick={addCell}>Nouvelle cellule</button>
                </div>
            </div>
        </div>
    )
}