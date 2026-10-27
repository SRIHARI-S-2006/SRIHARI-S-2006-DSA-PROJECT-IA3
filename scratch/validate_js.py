import subprocess

js_code = """
async function loadPortfolioHealthGauge() {
  const canvas = document.getElementById("portfolioHealthGaugeChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (chartInstances.portfolioHealthGauge) chartInstances.portfolioHealthGauge.destroy();
  chartInstances.portfolioHealthGauge = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Safe Zone (<20%)", "Industry Benchmark (20-25%)", "Elevated Churn (25-35%)", "Remaining"],
      datasets: [{
        data: [20, 5, 10, 65],
        backgroundColor: ["#10b981", "#f59e0b", "#f43f5e", "rgba(255, 255, 255, 0.05)"],
        borderWidth: 0,
        circumference: 180,
        rotation: -90
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => `${c.label}: ${c.raw}%`
          }
        }
      },
      cutout: "78%"
    }
  });
}
console.log("Syntax test passed!");
"""

with open("scratch/test_js_syntax.mjs", "w", encoding="utf-8") as f:
    f.write(js_code)

res = subprocess.run(["node", "scratch/test_js_syntax.mjs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
