/**
 * CineVerse — Main JavaScript
 * Hero particles animation
 */
document.addEventListener('DOMContentLoaded', () => {
    // Create floating particles in the hero section
    const particleContainer = document.getElementById('hero-particles');
    if (particleContainer) {
        createParticles(particleContainer, 30);
    }
});

/**
 * Generate floating particle elements for visual ambience.
 */
function createParticles(container, count) {
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        const size = Math.random() * 4 + 1;
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        const duration = Math.random() * 20 + 10;
        const delay = Math.random() * 10;
        const opacity = Math.random() * 0.3 + 0.1;

        Object.assign(particle.style, {
            position: 'absolute',
            width: `${size}px`,
            height: `${size}px`,
            borderRadius: '50%',
            background: `rgba(168, 85, 247, ${opacity})`,
            left: `${x}%`,
            top: `${y}%`,
            animation: `particleFloat ${duration}s ease-in-out ${delay}s infinite`,
            pointerEvents: 'none',
        });

        container.appendChild(particle);
    }

    // Inject keyframes once
    if (!document.getElementById('particle-keyframes')) {
        const style = document.createElement('style');
        style.id = 'particle-keyframes';
        style.textContent = `
            @keyframes particleFloat {
                0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
                25% { transform: translate(30px, -40px) scale(1.2); opacity: 0.6; }
                50% { transform: translate(-20px, -80px) scale(0.8); opacity: 0.4; }
                75% { transform: translate(40px, -40px) scale(1.1); opacity: 0.5; }
            }
        `;
        document.head.appendChild(style);
    }
}
