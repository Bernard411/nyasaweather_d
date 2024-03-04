// Select the toggle button and colors
const toggleButton = document.querySelector('.dark-light');
const colors = document.querySelectorAll('.color');

// Function to toggle between dark and light modes
const toggleDarkMode = () => {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
};

// Function to set the selected color theme
const setColorTheme = (theme) => {
    colors.forEach(c => c.classList.remove('selected'));
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('colorTheme', theme);
};

// Event listeners
colors.forEach(color => {
    color.addEventListener('click', e => {
        const theme = color.getAttribute('data-color');
        setColorTheme(theme);
        color.classList.add('selected');
    });
});

toggleButton.addEventListener('click', () => {
    toggleDarkMode();
});

// Check local storage for dark mode and color theme preferences
document.addEventListener('DOMContentLoaded', () => {
    const isDarkMode = localStorage.getItem('darkMode');
    if (isDarkMode === 'true') {
        document.body.classList.add('dark-mode');
    }

    const colorTheme = localStorage.getItem('colorTheme');
    if (colorTheme) {
        setColorTheme(colorTheme);
        const selectedColor = document.querySelector(`[data-color="${colorTheme}"]`);
        selectedColor.classList.add('selected');
    }
});
