document.addEventListener("DOMContentLoaded", () => {
    const fraudDropdown = document.getElementById("fraud-dropdown");
    const amountSlider = document.getElementById("amount-slider");

    // Update visualizations based on filters
    const updateVisualizations = async () => {
        const fraudClass = fraudDropdown.value;
        const amountRange = amountSlider.value;

        try {
            // Fetch data from the generated JSON files
            const [fraudPieData, heatmapData, scatterData, scatter3DData] = await Promise.all([
                fetch('fraud_pie_chart.json').then(response => response.json()),
                fetch('heatmap.json').then(response => response.json()),
                fetch('time_amount_scatter.json').then(response => response.json()),
                fetch('scatter_3d.json').then(response => response.json())
            ]);

            // Update Pie Chart
            Plotly.newPlot("fraud-pie-chart", fraudPieData);

            // Update Heatmap
            Plotly.newPlot("heatmap", heatmapData);

            // Update Scatter Plot
            Plotly.newPlot("time-amount-scatter", scatterData);

            // Update 3D Scatter Plot
            Plotly.newPlot("3d-scatter-v1-v2-amount", scatter3DData);
        } catch (error) {
            console.error("Error fetching or updating visualizations:", error);
        }
    };

    // Event listeners for filters
    fraudDropdown.addEventListener("change", updateVisualizations);
    amountSlider.addEventListener("input", updateVisualizations);

    // Initial render
    updateVisualizations();
});
