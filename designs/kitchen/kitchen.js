function toggleHeart(icon) {
    if (icon.classList.contains('fa-heart-o')) {
        icon.classList.remove('fa-heart-o');
        icon.classList.add('fa-heart');
    } else {
        icon.classList.remove('fa-heart');
        icon.classList.add('fa-heart-o');
    }
}
