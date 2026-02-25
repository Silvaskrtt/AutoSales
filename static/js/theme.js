// Toggle tema claro/escuro
document.getElementById('btn-tema').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
    const lightIcon = document.querySelector('.theme-toggle-light');
    const darkIcon = document.querySelector('.theme-toggle-dark');
    if (document.body.classList.contains('dark-mode')) {
        lightIcon.style.display = 'none';
        darkIcon.style.display = 'inline';
    } else {
        lightIcon.style.display = 'inline';
        darkIcon.style.display = 'none';
    }
});