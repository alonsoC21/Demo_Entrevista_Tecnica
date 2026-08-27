document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://localhost:8000/api/progreso/1';
    let chartInstance = null; // Guardar referencia para evitar duplicados en re-renders

    // Función principal orquestadora
    async function initDashboard() {
        try {
            const data = await fetchProgreso();
            renderKPIs(data);
            renderChart(data.historial_semana);
        } catch (error) {
            showError("No se pudo conectar con el servidor. Verifica que la API esté corriendo.");
            console.error("Fetch Error:", error);
        }
    }

    // Petición al backend
    async function fetchProgreso() {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    // Actualización del DOM
    function renderKPIs(data) {
        document.getElementById('kpi-terminados').textContent = data.cursos_terminados;
        document.getElementById('kpi-racha').textContent = data.racha_dias;
        
        // Sumar todas las horas del arreglo
        const horasTotales = data.historial_semana.reduce((acc, dia) => acc + dia.total_horas, 0);
        document.getElementById('kpi-horas').textContent = horasTotales.toFixed(1);
    }

    // Renderizado de Chart.js
    function renderChart(historial) {
        const ctx = document.getElementById('progresoChart').getContext('2d');
        
        // Mapear datos para la gráfica
        const labels = historial.map(item => item.fecha);
        const dataValues = historial.map(item => item.total_horas);

        // Si ya existe una gráfica, la destruimos antes de crear una nueva
        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Horas Dedicadas',
                    data: dataValues,
                    backgroundColor: '#4f46e5',
                    borderRadius: 6,
                    barThickness: 40
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false } 
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Horas' }
                    }
                }
            }
        });
    }

    // Manejo de UI en caso de error
    function showError(message) {
        const errorDiv = document.getElementById('error-alert');
        errorDiv.textContent = message;
        errorDiv.className = 'alert-error';
    }

    // Ejecutar al cargar
    initDashboard();
});