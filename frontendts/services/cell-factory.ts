import {Cell} from "../models/cells";

export class CellFactory {

    private static _lastId = 0;

    private static get nextId(): number {
        CellFactory._lastId += 1;
        return CellFactory._lastId;
    }

    static createCell(): Cell {
        return {
            id: CellFactory.nextId,
            content: ""
        }
    }
}
