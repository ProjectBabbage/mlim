import {Cell} from "../models/cells";
import Line from "./Line";

interface CellProps {
    cell: Cell;
}

export default function CellComponent(props: CellProps) {
    return (
        <div>
            <h2>Cell</h2>
            { props.cell.lines.map((line, i) => <Line line={line} key={i}></Line>) }
        </div>
    )
}