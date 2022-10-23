import {ChartProps} from "../../models/chart-props";

export function getDefaultProps(): ChartProps {
    const data: [number, number][] = [];
    for(let i = 0.1; i < 1000; i += 0.1) {
        data.push([i, 30 * Math.log(i)]);
    }

    return {
        data: data,
        points: [[10, 30], [40, 50], [45, 12]],
        xMargin: 40,
        yMargin: 40,
        width: 720,
        height: 300,
    };
}