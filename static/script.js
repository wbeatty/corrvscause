const graphContainer = document.querySelector(".graphContainer");
const graphBtn = document.getElementById("loadGraphButton");
const chartTitle = document.querySelector(".graphTitle");

async function getRandomPairing() {
  const response = await fetch("/api/pairings/random");
  const data = await response.json();
  return data;
}

async function showGraph() {
  const data = await getRandomPairing();
  graphContainer.innerHTML = `
  <div class="graphTitle">
  <h2>${data.dataset1.name} vs ${data.dataset2.name}</h2>
  </div>
        <div class="graphCanvas">
          <canvas id="myChart"> </canvas>
        </div>
        <div class="btnContainer">
          <button class="iconBtn">
            <p>Correlation</p>
          </button>
          <button class="iconBtn">
            <p>Causation</p>
          </button>
  `;
  new Chart(document.getElementById("myChart"), {
    type: "line",
    options: {
      responsive: true,
    },
    data: {
      labels: data.dataset1.years,
      datasets: [
        {
          label: data.dataset1.name,
          data: data.dataset1.values,
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          fill: true,
        },
        {
          label: data.dataset2.name,
          data: data.dataset2.values,
          borderColor: "rgba(153, 102, 255, 1)",
          backgroundColor: "rgba(153, 102, 255, 0.2)",
          fill: true,
        },
      ],
      scales: {
        x: {
          grid: {
            display: false,
          },
        },
        y: {
          grid: {
            display: false,
          },
        },
      },
    },
  });
}

graphBtn.addEventListener("click", showGraph);
