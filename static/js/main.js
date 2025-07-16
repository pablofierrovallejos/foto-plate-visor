// Plate Track Talcahuano - Scripts principales

// Función para establecer fechas por defecto
function setDefaultDates() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const todayDate = `${year}-${month}-${day}`;
    
    // Setear fecha en el formulario principal
    const mainDateInput = document.getElementById('date');
    if (mainDateInput && !mainDateInput.value) {
        mainDateInput.value = todayDate;
    }
    
    // Setear fechas en el formulario de filtros
    const dateInput = document.querySelector('input[name="date"]');
    if (dateInput && !dateInput.value) {
        dateInput.value = todayDate;
    }
    
    const dateEndInput = document.querySelector('input[name="date_end"]');
    if (dateEndInput && !dateEndInput.value) {
        dateEndInput.value = todayDate;
    }
}

// Función para manejar el botón de gráfico
function handleChartButton() {
    const chartButton = document.getElementById('chartButton');
    if (chartButton) {
        chartButton.addEventListener('click', function (event) {
            event.preventDefault();
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            const todayDate = `${year}-${month}-${day}`;
            
            window.location.href = `/chart?date=${todayDate}`;
        });
    }
}

// Función para recargar YouTube Live
function reloadYouTubeLive() {
    const container = document.getElementById('youtube-live-container');
    if (container) {
        const ytSrc = "https://www.youtube.com/embed/live_stream?channel=UCTPMBs1bIGCE1q13JgGXzHQ&autoplay=1&mute=1&t=" + Date.now();
        container.innerHTML = `
            <iframe width="550" height="310" src="${ytSrc}" title="Live session" frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        `;
    }
}

// Función para manejar zoom de imágenes
function handleImageZoom() {
    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('zoomable-image')) {
            event.stopPropagation();
            // Si es imagen PiP (Picture in Picture)
            if (event.target.alt === "Picture in Picture") {
                event.target.classList.toggle('zoomed-pip');
            } else {
                event.target.classList.toggle('zoomed-image');
            }
        }
    });
}

// Función para debugging (clicks)
function enableDebugMode() {
    document.addEventListener('click', function (event) {
        console.log('Elemento clickeado:', event.target);
    });
}

// Función para manejar navegación del header
function handleHeaderNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const loginBtn = document.querySelector('.login-btn');
    const currentPath = window.location.pathname;
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Handle login button active state
    if (loginBtn && currentPath === '/login') {
        loginBtn.classList.add('active');
    } else if (loginBtn) {
        loginBtn.classList.remove('active');
    }
}

// Función para manejar la recarga del video cuando se vuelve a la pestaña
function handleVisibilityChange() {
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            reloadYouTubeLive();
        }
    });
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    setDefaultDates();
    handleChartButton();
    handleImageZoom();
    handleHeaderNavigation();
    handleVisibilityChange();
    reloadYouTubeLive();
    
    // Habilitar modo debug solo en desarrollo
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        enableDebugMode();
    }
});
