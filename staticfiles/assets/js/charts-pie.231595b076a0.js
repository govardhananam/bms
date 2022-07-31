/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */

 const data = JSON.parse(document.getElementById('data').textContent);
 const labels = JSON.parse(document.getElementById('labels').textContent);

const pieConfig = {
  type: 'doughnut',
  data: {
    datasets: [
      {
        data: data,
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: ['#0694a2', '#1c64f2'],
        label: 'Boookings',
      },
    ],
    labels: labels,
  },
  options: {
    responsive: true,
    /**
     * Default legends are ugly and impossible to style.
     * See examples in charts.html to add your own legends
     *  */
    legend: {
      display: false,
    },
  },
}

// change this to the id of your chart element in HMTL
const pieCtx = document.getElementById('pie')
window.myPie = new Chart(pieCtx, pieConfig)
