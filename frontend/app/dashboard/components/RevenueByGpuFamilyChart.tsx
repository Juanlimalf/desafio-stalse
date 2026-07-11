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

export function RevenueByGpuFamilyChart({ data }: Readonly<Props>) {
  const chartData = toChartData(data);

  return (
    <div>
      <h2 className="mb-2 text-lg font-semibold text-gray-900">
        Receita por família de GPU
      </h2>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke={GRID_COLOR}
            vertical={false}
          />
          <XAxis dataKey="name" stroke={AXIS_COLOR} fontSize={12} />
          <YAxis
            stroke={AXIS_COLOR}
            fontSize={12}
            tickFormatter={(value) => compactCurrencyFormatter.format(value)}
          />
          <Tooltip
            formatter={(value) => currencyFormatter.format(Number(value))}
          />
          <Bar
            dataKey="value"
            fill={CATEGORICAL_COLORS[0]}
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
