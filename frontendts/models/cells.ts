export interface Cell {
    id: number;
    lines: Array<AbstractLine>;
}

interface Line {
    type: string;
    content: string;
}

export interface CodeLine extends Line {
    type: 'code';
}

export interface TextLine extends Line {
    type: 'text';
}

export type AbstractLine = CodeLine | TextLine;

