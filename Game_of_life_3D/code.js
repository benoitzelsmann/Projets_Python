

// Récupérer le bouton par son ID
const button = document.getElementById('btn');

// Ajouter un écouteur d'événements pour le clic sur le bouton
button.addEventListener('click', function () {
    // Afficher un message dans la console
    console.log('Le bouton a été cliqué !');

    // Modifier le texte du paragraphe
    const paragraph = document.querySelector('p');
    paragraph.textContent = 'Bravo ! Vous avez cliqué sur le bouton.';
});
