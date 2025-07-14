import Chart from "chart.js/auto";
import "./index.scss";

interface MakeChartType {
  utterances: string[];
  caretaker_percents: number[];
  child_percents: number[];
}

/** Takes values from server and generates staked bar plot. */
function makeChart({
  utterances,
  caretaker_percents,
  child_percents,
}: MakeChartType) {
  const ctx = document.querySelector<HTMLCanvasElement>("#chart");
  if (!ctx) {
    throw new Error("Canvas element not found.");
  }

  const data = {
    labels: utterances,
    datasets: [
      {
        label: "Caretaker",
        data: caretaker_percents,
        backgroundColor: "#ee4035",
      },
      {
        label: "Child",
        data: child_percents,
        backgroundColor: "#0392cf",
      },
    ],
  };

  new Chart(ctx, {
    type: "bar",
    data: data,
    options: {
      plugins: {
        title: {
          display: true,
          text: "Caretaker vs. Child Utterances",
        },
      },
      responsive: true,
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true,
        },
      },
    },
  });
}

/** Fetch session data from server and display chart. */
function displayChart() {
  fetch("/utterances")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Utterances response error: ${response.status}`);
      }
      return response.json();
    })
    .then((json) => {
      makeChart(json);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  displayChart();
});
