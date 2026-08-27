document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("path-form");
    const resultsContainer = document.getElementById("path-results");
    const timelineWrapper = document.getElementById("timeline-wrapper");
    const feedbackContainer = document.getElementById("feedback-container");
    const emptyState = document.getElementById("empty-state"); 
    const pathMeta = document.getElementById("path-meta");
    const totalHoursSpan = document.getElementById("total-hours");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        emptyState.classList.add('hidden'); 

        // Mantener la línea vertical al limpiar el contenedor
        const line = resultsContainer.querySelector('.timeline-line');
        resultsContainer.innerHTML = ''; 
        if(line) resultsContainer.appendChild(line);

        timelineWrapper.classList.add('hidden');
        feedbackContainer.classList.remove('hidden');
        feedbackContainer.innerHTML = '<p class="text-brand-blue font-medium animate-pulse">Generando tu ruta de aprendizaje...</p>';
        // Capturar valores
        const categoria = document.getElementById("categoria").value;
        const nivel = document.getElementById("nivel").value;

        try {
            const response = await fetch('/api/rutas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ categoria, nivel })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Error desconocido.");
            }

            // Actualizar metadatos y renderizar
            pathMeta.textContent = `${categoria} • Nivel ${nivel} • ${data.length} cursos`;
            renderTimeline(data);
            feedbackContainer.classList.add('hidden');

        } catch (error) {
            feedbackContainer.innerHTML = `<p class="text-red-500 font-medium bg-red-50 p-4 rounded-xl border border-red-100"> ${error.message}</p>`;
        }
    });

    function renderTimeline(courses) {
        timelineWrapper.classList.remove('hidden');
        let totalHours = 0;
        
        courses.forEach((course, index) => {
            totalHours += course.duracion_horas;
            const stepNumber = index + 1;
            
            // Contenedor relativo para el número y la tarjeta
            const itemDiv = document.createElement("div");
            itemDiv.className = "relative mb-6 last:mb-0";

            itemDiv.innerHTML = `
                <!-- Número del paso -->
                <div class="timeline-number">${stepNumber}</div>

                <!-- Tarjeta del Curso -->
                <div class="course-card">
                    <div class="flex justify-between items-start mb-3">
                        <h3 class="text-xl font-bold text-gray-900">${course.titulo}</h3>
                        <span class="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full">${course.duracion_horas} h</span>
                    </div>
                    
                    <p class="text-gray-600 text-base mb-4 leading-relaxed">${course.descripcion_breve}</p>
                    
                    <!-- Tags de metadatos -->
                    <div class="flex gap-2 text-sm text-gray-500">
                        <span>${course.categoria}</span>
                        <span>•</span>
                        <span>${course.nivel}</span>
                        <span>•</span>
                        <span>ID ${course.id}</span>
                    </div>
                </div>
            `;
            resultsContainer.appendChild(itemDiv);
        });

        // Actualizar total de horas
        totalHoursSpan.textContent = `${totalHours} horas en total`;
    }
});