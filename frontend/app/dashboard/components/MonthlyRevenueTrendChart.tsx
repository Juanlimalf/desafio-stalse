"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
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

export function MonthlyRevenueTrendChart({ data }: Readonly<Props>) {
  const chartData = toChartData(data);

  return (
    <div className="lg:col-span-2">
      <h2 className="mb-2 text-lg font-semibold text-gray-900">
        Tendência de receita mensal
      </h2>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={chartData}>
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
          <Line
            type="monotone"
            dataKey="value"
            stroke={CATEGORICAL_COLORS[0]}
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
