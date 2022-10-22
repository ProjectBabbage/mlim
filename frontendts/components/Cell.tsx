import {Cell} from "../models/cells";
import Line from "./Line";
import {useState} from "react";
import {LineFactory} from "../services/line-factory";

interface CellProps {
    id: number;
    cell: Cell;
}

export default function CellComponent(props: CellProps) {
    const [lines, setLines] = useState(props.cell.lines);

    function addLine(): void {
        const newLine = LineFactory.createCodeLine();
        setLines([...lines, newLine]);
    }

    return (
        <div className="cell-component">
            <h2>Cell #{props.id}</h2>
            { lines.map((line, i) => <div className="sick-fade-in" key={i}><Line line={line}></Line></div>) }
            <div className="action-container">
                <div className="flex-grow"></div>
                <button className="icon-button" type="button" onClick={addLine}>+</button>
            </div>
        </div>
    )
}