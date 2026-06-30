import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

import {
  FaBoxes,
  FaCheckCircle,
  FaPercentage,
  FaChartPie,
} from "react-icons/fa";

export default function Analytics({ result }) {
  if (!result) return null;

  const pieData = [
    { name: "Nestlé", value: result.nestle_count },
    { name: "Other", value: result.other_count },
  ];

  const barData = [
    { name: "Nestlé", count: result.nestle_count },
    { name: "Other", count: result.other_count },
  ];

  const COLORS = ["#22c55e", "#ef4444"];

  return (
    <section className="analytics-section">
      <div className="section-title">
        <h2>Analytics Dashboard</h2>
        <p>Brand share report generated from detected SKUs.</p>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <FaBoxes />
          <p>Total SKUs</p>
          <h3>{result.total}</h3>
        </div>

        <div className="kpi-card nestle">
          <FaCheckCircle />
          <p>Nestlé SKUs</p>
          <h3>{result.nestle_count}</h3>
        </div>

        <div className="kpi-card other">
          <FaBoxes />
          <p>Other SKUs</p>
          <h3>{result.other_count}</h3>
        </div>

        <div className="kpi-card">
          <FaPercentage />
          <p>Nestlé Share</p>
          <h3>{result.nestle_percent}%</h3>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>
            <FaChartPie /> Nestlé vs Other Share
          </h3>

          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                outerRadius={95}
                label
              >
                {pieData.map((_, index) => (
                  <Cell key={index} fill={COLORS[index]} />
                ))}
              </Pie>

              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Product Count Distribution</h3>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#2563eb" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="summary-card">
        <h3>Detection Summary</h3>

        <div className="summary-row">
          <span>Chiller Detected</span>
          <strong>{result.chiller_detected ? "Yes" : "No"}</strong>
        </div>

        <div className="summary-row">
          <span>Chiller Confidence</span>
          <strong>{result.chiller_confidence}%</strong>
        </div>

        <div className="summary-row">
          <span>Nestlé Share</span>
          <strong>{result.nestle_percent}%</strong>
        </div>

        <div className="progress-track">
          <div
            className="progress-fill nestle-fill"
            style={{ width: `${result.nestle_percent}%` }}
          />
        </div>

        <div className="summary-row">
          <span>Other Share</span>
          <strong>{result.other_percent}%</strong>
        </div>

        <div className="progress-track">
          <div
            className="progress-fill other-fill"
            style={{ width: `${result.other_percent}%` }}
          />
        </div>
      </div>
    </section>
  );
}