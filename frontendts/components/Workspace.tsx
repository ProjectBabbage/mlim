import REPL from "./Repl";
import { Dispatch, SetStateAction, useEffect, useState } from "react";

type CellsType = Array<JSX.Element>;
type OptCellsType = CellsType | null;
type UseState<S> = [S, Dispatch<SetStateAction<S>>];

export default function Workspace() {
  const [cells, setCells]: UseState<CellsType> = useState<CellsType>([]);
  const [cellCount, setCellCount]: UseState<number> = useState<number>(0);
  const [cellsDisplay, setCellsDisplay]: UseState<OptCellsType> =
    useState<OptCellsType>(null);

  useEffect(() => {
    console.log(cells);
    console.log("updated");
    setCellsDisplay(cells);
  }, [cellCount]);

  function addCell(): void {
    cells.push(
      <div key={cells.length}>
        CELL
        <REPL />
      </div>
    );
    setCellCount(cellCount + 1);
  }

  return (
    <div>
      <div>{cellsDisplay}</div>
      <div className="button" onClick={() => addCell()}>
        +
      </div>
    </div>
  );
}
