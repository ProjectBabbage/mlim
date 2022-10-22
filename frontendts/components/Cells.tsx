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
        setCells([...cells, newCell])
    }

    return (
        <div>
            <h2>My Cells</h2>
            <button type="button" onClick={addCell}>Nouvelle cellule</button>
            { cells.map((cell, i) => <CellComponent cell={cell} key={i}></CellComponent>) }
        </div>
    )
}