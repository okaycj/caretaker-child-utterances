/* colors: #ee4035 #f37736 #fdf498 #7bc043 #0392cf*/


function displayChart(utterance, careTakerPercent, childPercent, title) {
    const ctx = document.getElementById('chart');

    const data = {
        labels: [utterance],
        datasets: [{
            label: 'Care Taker',
            data: [careTakerPercent],
            backgroundColor: "#ee4035",
        }, {
            label: 'Child',
            data: [childPercent],
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
                    text: title
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