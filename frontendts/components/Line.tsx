import {AbstractLine} from "../models/cells";
import React from "react";

interface LineProps {
    line: AbstractLine;
}

export default class Line extends React.Component<LineProps, any> {
    constructor(props: LineProps) {
        super(props);

        this.state = {value: props.line.content};
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event: any): void {
        this.setState({value: event.target.value});
    }

    render() {
        return (
            <div>
                <textarea className="line-area" value={this.state.value} onChange={this.handleChange}></textarea>
            </div>
        )
    }
}