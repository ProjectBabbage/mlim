import REPL from './repl';
import { useEffect, useState } from 'react';

export default function Workspace() {
  const [cells, setCells] = useState([])
  const [cellCount, setCellCount] = useState(0)
  const [cellsDisplay, setCellsDisplay] = useState(null)

    useEffect(() => {
        console.log(cells)
        console.log("updated")
        setCellsDisplay(cells)
    }, [cellCount])

    function addCell(){
        cells.push(
            <div key={cells.length}>
                CELL
                <REPL/>
            </div>)
        setCellCount(cellCount + 1)
        console.log(cells.length)
    }

    return (
        <div>
            <div>
            {cellsDisplay}
            </div>
        <div 
            className="button"
            onClick={() => addCell()}
            >+</div>
        </div>
)
}
