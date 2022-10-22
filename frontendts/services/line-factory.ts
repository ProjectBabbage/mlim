import {CodeLine, TextLine} from "../models/cells";

export class LineFactory {
    static createCodeLine(): CodeLine {
        return {
            type: 'code',
            content: '',
        }
    }

    static createTextLine(): TextLine {
        return {
            type: 'text',
            content: '',
        }
    }
}