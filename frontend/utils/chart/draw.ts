import * as d3 from "d3";
import {ChartProps} from "../../models/chart-props";

export function draw(svg: d3.Selection<SVGSVGElement|null, unknown, null, undefined>, config: ChartProps): void {
    /**
     * Draw axis
     */
    const xAxis = svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(${config.xMargin},${config.yMargin + config.height})`)
    ;

    const scaleX = d3.scaleLinear()
        .domain([0.9 * Math.min(...config.data.map(data => data[0])), 1.1 * Math.max(...config.data.map(data => data[0]))])
        .range([0, config.width]);

    const x_axis = d3.axisBottom(scaleX);
    xAxis.call(x_axis);

    const yAxis = svg.append('g')
        .attr('class', 'y-axis')
        .attr('transform', `translate(${config.xMargin},${config.yMargin})`)
    ;

    const scaleY = d3.scaleLinear()
        .domain([1.1 * Math.max(...config.data.map(data => data[1])), 0.9 * Math.min(...config.data.map(data => data[1]))])
        .range([0, config.height])

    const y_axis = d3.axisLeft(scaleY);
    yAxis.call(y_axis);

    const view = svg.append("g")
        .attr("class", "view")
        .attr('transform', `translate(${config.xMargin},${config.yMargin})`)
        .attr("x", 0.5)
        .attr("y", 0.5)
        .attr("fill", "none")
        .attr("width", config.width - 1)
        .attr("height", config.height - 1);


    function zoomed({ transform }: {transform: any}) {
        view.attr("transform", transform);
        xAxis.call(x_axis.scale(transform.rescaleX(scaleX)));
        yAxis.call(y_axis.scale(transform.rescaleY(scaleY)));
    }

    function filter(event: any) {
        event.preventDefault();
        return (!event.ctrlKey || event.type === 'wheel') && !event.button;
    }

    const zoom = d3.zoom()
        .scaleExtent([1/4, 8])
        .translateExtent([[-100, -100], [config.width + 90, config.height + 100]])
        .filter(filter)
        .on("zoom", zoomed);

    // @ts-ignore
    svg.call(zoom);

    /**
     * Draw curve
     */
    const line = d3.line()
        .x(d => scaleX(d[0]))
        .y(d => scaleY(d[1]));

    view.append('path')
        .attr('d', line(config.data))
        .attr('fill', 'none')
        .attr('stroke', 'black')
        .attr('stroke-width', '1')
    ;

    /**
     * Draw points
     */
    const points = view.append('g')
        .attr('class', 'points')
    ;

    points.selectAll('.data-point').data(config.points)
        .enter()
        .append("circle")
        .attr('class', 'data-point')
        .attr("fill", "red")
        .attr("stroke", "none")
        .attr("cx", function(d) { return scaleX(d[0]) })
        .attr("cy", function(d) { return scaleY(d[1]) })
        .attr("r", 3)

    points.exit().remove();
}