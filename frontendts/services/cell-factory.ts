import {Cell} from "../models/cells";

export class CellFactory {
    static createCell(): Cell {
        return {
            lines: [],
        }
    }
}