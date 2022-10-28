import React from "react";
import * as d3 from "d3";
import {ChartProps} from "../models/chart-props";
import {getDefaultProps} from "../utils/chart/default-props";
import {draw} from "../utils/chart/draw";

function drawChart(svgRef: React.RefObject<SVGSVGElement>, props: Partial<ChartProps>) {
    const config = Object.assign(getDefaultProps(), props);
    const svg = d3.select(svgRef.current);

    svg.selectChildren().remove();
    svg
        .attr("width", config.width + 2 * config.xMargin)
        .attr("height", config.height + 2 * config.yMargin);

    draw(svg, config);
}

export default function Chart(props: Partial<ChartProps>) {
    const svgRef = React.useRef<SVGSVGElement>(null);

    React.useEffect(() => {
        drawChart(svgRef, props);
    }, [svgRef]);

    return (
        <div>
            <svg ref={svgRef}>
                <svg className="axis"></svg>
            </svg>
        </div>
    )
}