// Theme Switcher JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    
    // Check for saved theme preference or use the default theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    updateToggleIcon(savedTheme);
    
    // Add event listener to the toggle button
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Update the theme
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        
        // Save the preference
        localStorage.setItem('theme', newTheme);
        
        // Update the toggle icon and animate
        updateToggleIcon(newTheme);
        animateToggleIcon(newTheme);
        
        // Add a transition effect
        document.body.classList.add('theme-transition');
        setTimeout(() => {
            document.body.classList.remove('theme-transition');
        }, 300);
    });
    
    // Function to update the toggle icon based on the current theme
    function updateToggleIcon(theme) {
        if (theme === 'dark') {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        } else {
            themeToggle.innerHTML = `<svg class="custom-sun" width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:auto;">
                <circle cx="11" cy="11" r="5" stroke="currentColor" stroke-width="2" fill="none"/>
                <g stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <line x1="11" y1="1" x2="11" y2="4"/>
                    <line x1="11" y1="18" x2="11" y2="21"/>
                    <line x1="1" y1="11" x2="4" y2="11"/>
                    <line x1="18" y1="11" x2="21" y2="11"/>
                    <line x1="4.93" y1="4.93" x2="7.05" y2="7.05"/>
                    <line x1="14.95" y1="14.95" x2="17.07" y2="17.07"/>
                    <line x1="4.93" y1="17.07" x2="7.05" y2="14.95"/>
                    <line x1="14.95" y1="7.05" x2="17.07" y2="4.93"/>
                </g>
            </svg>`;
        }
    }

    // Function to animate the toggle icon
    function animateToggleIcon(theme) {
        if (theme === 'light') {
            themeToggle.classList.remove('moon-animate');
            themeToggle.classList.add('sun-animate');
            setTimeout(() => {
                themeToggle.classList.remove('sun-animate');
                themeToggle.classList.add('sun-glow');
            }, 700); // match sunSpinScale duration
        } else {
            themeToggle.classList.remove('sun-animate', 'sun-glow');
            themeToggle.classList.add('moon-animate');
            setTimeout(() => {
                themeToggle.classList.remove('moon-animate');
            }, 500);
        }
    }
}); 