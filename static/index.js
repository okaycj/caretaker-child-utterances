/** Takes values from server and generates staked bar plot. */
function makeChart({
    utterances,
    caretaker_percents,
    child_percents
}) {
    const ctx = document.getElementById('chart');

    const data = {
        labels: utterances,
        datasets: [{
            label: 'Caretaker',
            data: caretaker_percents,
            backgroundColor: "#ee4035",
        }, {
            label: 'Child',
            data: child_percents,
            backgroundColor: "#0392cf",
        }, ]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Caretaker vs. Child Utterances"
                },
            },
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true
                }
            }
        }
    };

    new Chart(ctx, config)
}

/** Fetch session data from server and display chart. */
function displayChart(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Utterances response error: ${response.status}`);
            }
            return response.json();
        }).then(json => {
            makeChart(json)
        });
}