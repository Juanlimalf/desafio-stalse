"use client";

import { Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { CATEGORICAL_COLORS, currencyFormatter, toChartData } from "./chartUtils";

type Props = {
  data: Record<string, number>;
};

export function RevenueBySalesChannelChart({ data }: Readonly<Props>) {
  const chartData = toChartData(data).map((entry, index) => ({
    ...entry,
    fill: CATEGORICAL_COLORS[index % CATEGORICAL_COLORS.length],
  }));

  return (
    <div>
      <h2 className="mb-2 text-lg font-semibold text-gray-900">
        Receita por canal de vendas
      </h2>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={2}
          />
          <Tooltip
            formatter={(value) => currencyFormatter.format(Number(value))}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
