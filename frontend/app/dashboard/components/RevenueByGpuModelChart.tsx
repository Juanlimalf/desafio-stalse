"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  AXIS_COLOR,
  CATEGORICAL_COLORS,
  GRID_COLOR,
  compactCurrencyFormatter,
  currencyFormatter,
  toChartData,
} from "./chartUtils";

type Props = {
  data: Record<string, number>;
};

export function RevenueByGpuModelChart({ data }: Readonly<Props>) {
  const chartData = toChartData(data).sort((a, b) => b.value - a.value);

  return (
    <div>
      <h2 className="mb-2 text-lg font-semibold text-gray-900">
        Receita por modelo de GPU
      </h2>
      <ResponsiveContainer width="100%" height={560}>
        <BarChart data={chartData} layout="vertical" margin={{ left: 24 }}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke={GRID_COLOR}
            horizontal={false}
          />
          <XAxis
            type="number"
            stroke={AXIS_COLOR}
            fontSize={12}
            tickFormatter={(value) => compactCurrencyFormatter.format(value)}
          />
          <YAxis
            type="category"
            dataKey="name"
            stroke={AXIS_COLOR}
            fontSize={12}
            width={100}
          />
          <Tooltip
            formatter={(value) => currencyFormatter.format(Number(value))}
          />
          <Bar
            dataKey="value"
            fill={CATEGORICAL_COLORS[3]}
            radius={[0, 4, 4, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
