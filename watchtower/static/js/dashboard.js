// ===== WATCHTOWER — DASHBOARD JS =====

// Live metric update every 3 seconds
function randomBetween(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function updateMetricDisplay(id, value) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = value + '%';
  }
  const barId = id.replace('val', 'bar');
  const bar = document.getElementById(barId);
  if (bar) bar.style.width = value + '%';

  const statusId = id.replace('val', 'status');
  const status = document.getElementById(statusId);
  if (status) {
    if (value < 50) status.textContent = 'Normal';
    else if (value < 75) status.textContent = 'Moderate';
    else status.textContent = 'High';
  }
}

// ===== LINE CHART =====
let lineChart;
function initLineChart(cpuHistory, ramHistory) {
  const ctx = document.getElementById('lineChart');
  if (!ctx) return;

  const labels = ['T-9', 'T-8', 'T-7', 'T-6', 'T-5', 'T-4', 'T-3', 'T-2', 'T-1', 'Now'];
  lineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'CPU %',
          data: cpuHistory,
          borderColor: '#00d4ff',
          backgroundColor: 'rgba(0,212,255,0.06)',
          fill: true,
          tension: 0.4,
          pointRadius: 3,
          pointBackgroundColor: '#00d4ff',
          borderWidth: 2,
        },
        {
          label: 'RAM %',
          data: ramHistory,
          borderColor: '#7c3aed',
          backgroundColor: 'rgba(124,58,237,0.06)',
          fill: true,
          tension: 0.4,
          pointRadius: 3,
          pointBackgroundColor: '#7c3aed',
          borderWidth: 2,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: '#64748b', font: { family: 'Space Grotesk', size: 12 } }
        }
      },
      scales: {
        x: {
          ticks: { color: '#334155', font: { family: 'JetBrains Mono', size: 11 } },
          grid: { color: 'rgba(30,45,61,0.6)' }
        },
        y: {
          min: 0, max: 100,
          ticks: { color: '#334155', font: { family: 'JetBrains Mono', size: 11 }, callback: v => v + '%' },
          grid: { color: 'rgba(30,45,61,0.6)' }
        }
      }
    }
  });
}

// ===== DONUT CHART =====
let donutChart;
function initDonutChart(cpu, ram, disk) {
  const ctx = document.getElementById('donutChart');
  if (!ctx) return;

  donutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['CPU', 'RAM', 'Disk'],
      datasets: [{
        data: [cpu, ram, disk],
        backgroundColor: ['rgba(0,212,255,0.8)', 'rgba(124,58,237,0.8)', 'rgba(16,185,129,0.8)'],
        borderColor: ['#00d4ff', '#7c3aed', '#10b981'],
        borderWidth: 2,
        hoverOffset: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#64748b', padding: 16, font: { family: 'Space Grotesk', size: 12 } }
        }
      }
    }
  });
}

// ===== LIVE UPDATE LOOP =====
function startLiveUpdates() {
  setInterval(() => {
    const cpu  = randomBetween(15, 92);
    const ram  = randomBetween(25, 88);
    const disk = randomBetween(35, 82);

    updateMetricDisplay('cpu-val', cpu);
    updateMetricDisplay('ram-val', ram);
    updateMetricDisplay('disk-val', disk);

    // Push to line chart
    if (lineChart) {
      lineChart.data.datasets[0].data.shift();
      lineChart.data.datasets[0].data.push(cpu);
      lineChart.data.datasets[1].data.shift();
      lineChart.data.datasets[1].data.push(ram);
      lineChart.update('none');
    }

    // Update donut
    if (donutChart) {
      donutChart.data.datasets[0].data = [cpu, ram, disk];
      donutChart.update('none');
    }
  }, 3000);
}
